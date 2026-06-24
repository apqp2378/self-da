"""Module A · Phase 2 전처리 — jd_raw → jd_clean.

입력 단위: JD 1건 = 1행 (jd_raw)
출력 단위: JD 1건 = 1행 (jd_clean) — 행 수 불변

설계 원칙:
- 원칙 2: 한 책임 한 함수. 정제 단계를 하위 함수로 분리하고 clean_jd에서 조합한다.
- 원칙 5: 입력·출력 단위를 docstring에 명시한다.
- 정제는 row를 삭제하지 않는다. 200자 미만은 too_short 플래그만 표시한다 (원칙 7).
- 결정론적 처리만 한다. LLM 호출 없음 (원칙 6).

외부 라이브러리: polars만 사용(파서와 동일). 정제는 표준 라이브러리 re/html로 처리.
"""
from __future__ import annotations

import html
import re

import polars as pl

MIN_TEXT_LEN = 200  # 이 미만이면 too_short=True (행은 유지)

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")
# 이모지·기타 기호(픽토그램) 영역. 한글/영문/숫자/일반 문장부호는 보존한다.
_EMOJI_RE = re.compile(
    "[\U0001f000-\U0001faff\U00002600-\U000027bf\U0001f1e6-\U0001f1ff"
    "\U00002190-\U000021ff\U0000fe00-\U0000fe0f]"
)
# 회사명 접두·접미 법인 표기. 정규화 시 제거한다.
_COMPANY_TOKEN_RE = re.compile(r"주식회사|유한회사|\(주\)|（주）|㈜|\(유\)")


def _strip_html(text: str) -> str:
    """HTML 태그 제거. 단위: 문자열 1개. 엔티티는 먼저 unescape한다."""
    return _HTML_TAG_RE.sub(" ", html.unescape(text))


def _remove_emoji(text: str) -> str:
    """이모지·픽토그램 제거. 단위: 문자열 1개. 한글/영문/숫자/문장부호는 보존."""
    return _EMOJI_RE.sub("", text)


def _collapse_whitespace(text: str) -> str:
    """연속 공백·개행을 단일 공백으로 접고 양끝 공백 제거. 단위: 문자열 1개."""
    return _WHITESPACE_RE.sub(" ", text).strip()


def clean_text(text: str | None) -> str | None:
    """원문 텍스트 → 정제 텍스트. 단위: 문자열 1개.

    None은 None으로 통과(결측은 명시적 None 유지, 파서와 동일 규칙).
    순서: 엔티티 unescape + 태그 제거 → 이모지 제거 → 공백 접기.
    """
    if text is None:
        return None
    cleaned = _collapse_whitespace(_remove_emoji(_strip_html(text)))
    return cleaned or None


def normalize_company(name: str | None) -> str | None:
    """회사명 정규화. 단위: 문자열 1개. 법인 표기(주식회사·(주)·㈜ 등) 제거 후 공백 정리."""
    if name is None:
        return None
    normalized = _collapse_whitespace(_COMPANY_TOKEN_RE.sub(" ", name))
    return normalized or None


def _build_analysis_text(
    responsibilities: str | None,
    requirements: str | None,
    preferred: str | None,
    body: str | None,
) -> str | None:
    """분석용 원문 결합. 단위: JD 1건.

    3개 섹션(주요업무/자격요건/우대사항)을 우선 결합한다. 모두 비면 body로 폴백한다.
    토픽·스킬 단계가 읽는 본문 텍스트의 출처를 한 곳으로 고정한다.
    """
    parts = [s for s in (responsibilities, requirements, preferred) if s]
    if parts:
        return "\n".join(parts)
    return body


def clean_jd(jd_raw: pl.DataFrame) -> pl.DataFrame:
    """jd_raw → jd_clean.

    입력 단위: JD 1건 = 1행 (jd_raw)
    출력 단위: JD 1건 = 1행 (jd_clean) — 행 수 불변

    추가 컬럼:
        company_norm : 법인 표기 제거한 회사명
        text_clean   : 분석용 정제 텍스트(섹션 결합, 없으면 body) — 태그·이모지·공백 정제
        too_short    : text_clean 길이 < MIN_TEXT_LEN 이면 True (행은 삭제하지 않음)
    """
    analysis_raw = pl.struct(
        ["responsibilities", "requirements", "preferred", "body"]
    ).map_elements(
        lambda s: _build_analysis_text(
            s["responsibilities"], s["requirements"], s["preferred"], s["body"]
        ),
        return_dtype=pl.Utf8,
    )

    out = jd_raw.with_columns(
        pl.col("company")
        .map_elements(normalize_company, return_dtype=pl.Utf8)
        .alias("company_norm"),
        analysis_raw.map_elements(clean_text, return_dtype=pl.Utf8).alias("text_clean"),
    )
    out = out.with_columns(
        (pl.col("text_clean").str.len_chars().fill_null(0) < MIN_TEXT_LEN).alias(
            "too_short"
        )
    )
    if out.height != jd_raw.height:
        raise AssertionError("clean_jd는 행 수를 바꾸지 않아야 한다 (원칙 5)")
    return out
