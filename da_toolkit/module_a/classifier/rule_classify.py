"""Module A · Phase 3 분류 — jd_clean + label_rules → jd_label.

입력 단위: JD 1건 = 1행 (jd_clean)
출력 단위: JD 1건 = 1행 + label / label_score (행 수 불변)

BERTopic(비지도)을 파이프라인 단계에서 빼고 규칙 기반 분류로 대체한다 (D-006).
- 근거: JD 코퍼스가 작고 동질적이라 비지도 클러스터가 불안정하고, 라벨 후보가
  docs/domain_taxonomy.md에 이미 정의됨 → "발견"이 아니라 "매핑" 문제.
- 분류는 결정론적. LLM 호출 안 함 (원칙 6).
- 매핑 안 되는 JD는 강제 배정하지 않고 unknown으로 둔다 (원칙 7).

매칭 모델(가중 점수 + priority 타이브레이크):
    도메인 일치 +DOMAIN_W, 직군(job_category) 일치 +JC_W, 본문 키워드 1개당 +KW_W(상한 KW_CAP).
    단, 역할 신호(직군 또는 키워드)가 하나도 없으면 도메인만으로는 라벨을 주지 않는다.
    최고 점수 라벨을 고르고, 동점이면 priority가 낮은(=상위) 라벨을 택한다.
    어느 라벨도 자격을 못 얻으면 fallback_label(기본 'unknown').
"""
from __future__ import annotations

from pathlib import Path

import polars as pl

DOMAIN_W = 2
JC_W = 2
KW_W = 1
KW_CAP = 3  # 키워드 점수 상한 (특정 라벨이 키워드 수로 과대평가되는 것 방지)


def load_label_rules(path) -> dict:
    """label_rules.yaml → dict. 단위: 설정 파일 1개. (yaml 의존은 여기서만)"""
    import yaml

    with open(Path(path), encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalize_domain(industry: str | None, industry_normalize: dict) -> str | None:
    """industry 원문 → taxonomy 표준 도메인. 단위: 문자열 1개.

    표기 흔들림을 흡수하려고 부분일치(키가 industry에 포함)로 본다. 못 찾으면 None.
    """
    if not industry:
        return None
    low = industry.casefold()
    for token, domain in industry_normalize.items():
        if str(token).casefold() in low:
            return domain
    return None


def _any_hit(text: str, needles) -> int:
    """text 안에 needles 중 몇 개가 등장하는지. 단위: 문자열 1개. 대소문자 무시."""
    low = text.casefold()
    return sum(1 for n in needles if str(n).casefold() in low)


def _score_label(domain: str | None, job_category: str, text: str, label: dict) -> int:
    """단일 라벨에 대한 JD의 적합 점수. 단위: (JD 1건 × 라벨 1개).

    역할 신호(직군 또는 키워드)가 0이면 0점(=자격 없음). 도메인만으로는 라벨을 주지 않는다.
    """
    jc_hit = _any_hit(job_category, label.get("job_category_any", [])) if job_category else 0
    kw_hit = _any_hit(text, label.get("body_keywords_any", [])) if text else 0
    if jc_hit == 0 and kw_hit == 0:
        return 0

    domains = label.get("domains") or []
    domain_match = 1 if (domain and domain in domains) else 0
    return (
        DOMAIN_W * domain_match
        + JC_W * (1 if jc_hit else 0)
        + KW_W * min(kw_hit, KW_CAP)
    )


def _classify_row(domain, job_category, text, labels, fallback) -> dict:
    """한 JD를 라벨에 배정. 단위: JD 1건. priority 낮은 라벨이 동점 우선.

    출력: {"label": str, "label_score": int}
    """
    job_category = job_category or ""
    text = text or ""
    best_label, best_score, best_priority = fallback, 0, None
    for label in labels:
        score = _score_label(domain, job_category, text, label)
        if score <= 0:
            continue
        priority = label.get("priority", 999)
        if score > best_score or (score == best_score and priority < best_priority):
            best_label, best_score, best_priority = label["name"], score, priority
    return {"label": best_label, "label_score": best_score}


def classify_jd(jd_clean: pl.DataFrame, label_rules: dict) -> pl.DataFrame:
    """jd_clean → jd_label.

    입력 단위: JD 1건 = 1행 (jd_clean; text_clean 컬럼 사용)
    출력 단위: JD 1건 = 1행 + label / label_score  (행 수 불변)

    추가 컬럼:
        label       : 배정된 taxonomy 라벨 (없으면 fallback_label, 기본 'unknown')
        label_score : 매칭 점수 (사람 검수용 보조 지표, 원칙 7). 0이면 unknown.
    """
    industry_normalize = label_rules.get("industry_normalize", {})
    labels = label_rules.get("labels", [])
    fallback = label_rules.get("fallback_label", "unknown")

    out = jd_clean.with_columns(
        pl.col("industry")
        .map_elements(
            lambda v: normalize_domain(v, industry_normalize), return_dtype=pl.Utf8
        )
        .alias("domain")
    )
    assigned = pl.struct(["domain", "job_category", "text_clean"]).map_elements(
        lambda s: _classify_row(
            s["domain"], s["job_category"], s["text_clean"], labels, fallback
        ),
        return_dtype=pl.Struct({"label": pl.Utf8, "label_score": pl.Int64}),
    )
    out = out.with_columns(assigned.alias("_assigned")).unnest("_assigned")

    if out.height != jd_clean.height:
        raise AssertionError("classify_jd는 행 수를 바꾸지 않아야 한다 (원칙 5)")
    return out
