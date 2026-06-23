"""Module A · Phase 1 수집기 — 수동 수집 마크다운 → jd_raw.

입력 단위: data/raw/manual/YYYYMMDD/{회사}_{게시일}_{직무}.md  1파일 = JD 1건
출력 단위: JD 1건 = 1행 (jd_raw)

설계 원칙:
- 원칙 2: 한 책임 한 함수.
- 원칙 5: 입력·출력 단위를 함수 docstring에 명시한다.
- jd_raw는 "원문을 그대로 담는" 단계다. 스킬·토픽 등 파이프라인이 계산하는 값은 넣지 않는다.
- 중복은 삭제하지 않고 is_duplicate 플래그로 표시한다.

외부 라이브러리: python-frontmatter(파싱), polars(데이터)만 사용.
"""
from __future__ import annotations

import hashlib
import re
from datetime import date, datetime
from pathlib import Path

import frontmatter
import polars as pl

# 본인이 수집 단계에서 채우는 스칼라 메타데이터 키
SCALAR_KEYS = [
    "company", "title", "posted_date", "source_url",
    "employment_type", "experience_level", "experience_years",
    "education", "location", "industry", "job_category",
    "salary", "deadline", "team",
]
REQUIRED_KEYS = ["company", "title", "posted_date", "source_url"]

# 본문 섹션 고정 헤더 → 표준 컬럼명 (동의어 허용)
SECTION_HEADERS = {
    "responsibilities": ["주요업무", "담당업무", "업무내용"],
    "requirements": ["자격요건", "지원자격", "필수요건", "필수자격"],
    "preferred": ["우대사항", "우대요건", "preferred"],
}

# 파일명 패턴: {회사}_{YYYY-MM-DD}_{직무}
FILENAME_RE = re.compile(r"^(?P<company>.+?)_(?P<posted_date>\d{4}-\d{2}-\d{2})_(?P<title>.+)$")

# jd_raw 컬럼 → polras 타입 (None이 섞여도 컬럼 타입을 고정)
JD_RAW_SCHEMA: dict[str, pl.DataType] = {
    "jd_id": pl.Utf8,
    "company": pl.Utf8,
    "title": pl.Utf8,
    "posted_date": pl.Date,
    "source_url": pl.Utf8,
    "employment_type": pl.Utf8,
    "experience_level": pl.Utf8,
    "experience_years": pl.Utf8,
    "education": pl.Utf8,
    "location": pl.Utf8,
    "industry": pl.Utf8,
    "job_category": pl.Utf8,
    "salary": pl.Utf8,
    "deadline": pl.Utf8,
    "team": pl.Utf8,
    "responsibilities": pl.Utf8,
    "requirements": pl.Utf8,
    "preferred": pl.Utf8,
    "body": pl.Utf8,
    "collected_date": pl.Date,
    "source_file": pl.Utf8,
    "dedup_key": pl.Utf8,
}


class JDParseError(ValueError):
    """파일명·frontmatter·폴더명 규칙 위반."""


def _normalize_header(line: str) -> str:
    """헤더 후보 라인을 정규화 (#, [], :, 공백 제거 후 소문자). 단위: 라인 1개."""
    return line.strip().strip("#[]").strip().rstrip(":").strip().lower()


def _split_sections(body: str) -> dict[str, str | None]:
    """본문 → {responsibilities, requirements, preferred}. 단위: JD 1건.

    고정 헤더(예: '## 주요업무', '[자격요건]', '우대사항:')로 분리한다.
    해당 헤더가 없으면 그 섹션은 None.
    """
    kw2canon = {kw.lower(): canon for canon, kws in SECTION_HEADERS.items() for kw in kws}
    sections: dict[str, list[str]] = {k: [] for k in SECTION_HEADERS}
    current: str | None = None
    for line in body.splitlines():
        key = _normalize_header(line)
        # 짧은 라인만 헤더로 인정 (긴 문장 오탐 방지)
        if key in kw2canon and len(line.strip()) <= 30:
            current = kw2canon[key]
            continue
        if current is not None:
            sections[current].append(line)
    return {k: ("\n".join(v).strip() or None) for k, v in sections.items()}


def _parse_date(value, path: Path) -> date:
    """frontmatter posted_date 값 → date. 단위: JD 1건."""
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value).strip(), "%Y-%m-%d").date()
    except ValueError as e:
        raise JDParseError(f"{path.name}: posted_date '{value}' 가 YYYY-MM-DD 형식이 아님") from e


def _collected_date_from_path(path: Path) -> date:
    """상위 폴더명 YYYYMMDD → collected_date. 단위: 파일 1개."""
    folder = path.parent.name
    try:
        return datetime.strptime(folder, "%Y%m%d").date()
    except ValueError as e:
        raise JDParseError(f"{path}: 상위 폴더명이 YYYYMMDD 형식이 아님 ('{folder}')") from e


def _dedup_key(company: str, posted_date: date, body: str) -> str:
    """회사 + 게시일 + 본문 앞 200자 → SHA1. 단위: JD 1건."""
    base = f"{company}|{posted_date}|{(body or '')[:200]}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


def parse_jd_file(path) -> dict:
    """단일 마크다운 파일 → jd_raw 행 1개(dict).

    입력 단위: 파일 1개 = JD 1건
    출력 단위: JD 1건 = dict 1개 (JD_RAW_SCHEMA 키)
    """
    path = Path(path)
    if not FILENAME_RE.match(path.stem):
        raise JDParseError(
            f"{path.name}: 파일명이 '{{회사}}_{{YYYY-MM-DD}}_{{직무}}.md' 패턴 위반"
        )

    post = frontmatter.load(path)
    meta = post.metadata
    body = (post.content or "").strip()

    missing = [k for k in REQUIRED_KEYS if not meta.get(k)]
    if missing:
        raise JDParseError(f"{path.name}: 필수 frontmatter 누락 {missing}")

    # 스칼라 필드: 빈 값은 명시적 None
    row: dict = {
        k: (str(meta[k]).strip() if meta.get(k) not in (None, "") else None)
        for k in SCALAR_KEYS
    }
    row["posted_date"] = _parse_date(meta.get("posted_date"), path)
    row["body"] = body or None
    row.update(_split_sections(body))  # responsibilities / requirements / preferred
    row["collected_date"] = _collected_date_from_path(path)
    row["source_file"] = str(path)
    row["dedup_key"] = _dedup_key(row["company"], row["posted_date"], body)
    row["jd_id"] = row["dedup_key"][:12]
    return row


def parse_manual_dir(input_dir, recursive: bool = True) -> pl.DataFrame:
    """수동 수집 폴더 → jd_raw DataFrame.

    입력 단위: data/raw/manual/YYYYMMDD/*.md  각 파일 = JD 1건
    출력 단위: JD 1건 = 1행 (jd_raw). 중복은 삭제하지 않고 is_duplicate 컬럼으로 표시.
    """
    input_dir = Path(input_dir)
    files = sorted(input_dir.rglob("*.md") if recursive else input_dir.glob("*.md"))
    if not files:
        raise JDParseError(f"{input_dir}: .md 파일이 없음")

    rows = [parse_jd_file(f) for f in files]
    df = pl.DataFrame(rows, schema=JD_RAW_SCHEMA)
    # 첫 등장은 is_duplicate=False, 이후 동일 dedup_key는 True (행은 유지)
    df = df.with_columns(
        (~pl.col("dedup_key").is_first_distinct()).alias("is_duplicate")
    )
    return df


def write_jd_raw(df: pl.DataFrame, out_path="data/interim/jd_raw.parquet") -> Path:
    """jd_raw DataFrame → Parquet. 단위 불변(JD 1건 = 1행)."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(out)
    return out


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="수동 수집 마크다운 → jd_raw.parquet")
    ap.add_argument("input_dir", help="예: data/raw/manual")
    ap.add_argument("-o", "--out", default="data/interim/jd_raw.parquet")
    args = ap.parse_args()

    df = parse_manual_dir(args.input_dir)
    out = write_jd_raw(df, args.out)
    n_dup = int(df["is_duplicate"].sum())
    print(f"JD {df.height}건 → {out} (중복 {n_dup}건 표시, 행 유지)")


if __name__ == "__main__":
    main()
