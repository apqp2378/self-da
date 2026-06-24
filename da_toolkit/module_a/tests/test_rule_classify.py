"""rule_classify.py 검증 — 도메인 정규화 + 가중 점수 + unknown 폴백 + 행 수 불변.

검증 단위: 문자열 1개(하위 함수) / JD 1건=1행(classify_jd).
"""
from pathlib import Path

import polars as pl

from da_toolkit.module_a.classifier import rule_classify as rc

RULES_PATH = (
    Path(__file__).parents[1] / "classifier" / "label_rules.yaml"
)


def _rules():
    return rc.load_label_rules(RULES_PATH)


def test_normalize_domain_substring():
    norm = {"이커머스": "이커머스", "커머스": "이커머스", "핀테크": "핀테크/금융"}
    assert rc.normalize_domain("이커머스/리테일", norm) == "이커머스"
    assert rc.normalize_domain("핀테크", norm) == "핀테크/금융"
    assert rc.normalize_domain("교육", norm) is None
    assert rc.normalize_domain(None, norm) is None


def test_ecommerce_growth_assigned():
    df = pl.DataFrame(
        {
            "industry": ["이커머스"],
            "job_category": ["프로덕트 데이터 분석가"],
            "text_clean": ["구매 전환율과 리텐션, 코호트, A/B테스트 기반 그로스 분석"],
        }
    )
    out = rc.classify_jd(df, _rules())
    assert out["label"][0] == "이커머스 그로스 분석"
    assert out["label_score"][0] > 0
    assert out.height == 1


def test_marketing_role_at_ecommerce_not_growth():
    # 설계 근거 케이스: 이커머스 회사의 마케팅 분석가 → '마케팅·캠페인'이어야 함
    df = pl.DataFrame(
        {
            "industry": ["이커머스"],
            "job_category": ["마케팅 데이터 분석가"],
            "text_clean": ["캠페인 유입과 ROAS, 광고 어트리뷰션, LTV 분석"],
        }
    )
    out = rc.classify_jd(df, _rules())
    assert out["label"][0] == "마케팅·캠페인 분석"


def test_no_role_signal_is_unknown():
    # 도메인만 맞고 역할 신호(직군/키워드) 없음 → 강제 배정 금지, unknown (원칙 7)
    df = pl.DataFrame(
        {
            "industry": ["이커머스"],
            "job_category": ["백엔드 엔지니어"],
            "text_clean": ["Kafka, Kubernetes, 서버 인프라 운영"],
        }
    )
    out = rc.classify_jd(df, _rules())
    assert out["label"][0] == "unknown"
    assert out["label_score"][0] == 0


def test_row_count_preserved_with_missing_fields():
    df = pl.DataFrame(
        {
            "industry": [None, "마케팅"],
            "job_category": [None, "퍼포먼스 마케터"],
            "text_clean": [None, "캠페인 ROAS 광고 분석"],
        }
    )
    out = rc.classify_jd(df, _rules())
    assert out.height == 2  # 결측 있어도 행 삭제 안 함
    assert out["label"][0] == "unknown"  # 신호 전무
