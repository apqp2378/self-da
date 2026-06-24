"""clean.py 검증 — 정제 규칙 + 행 수 불변 + too_short 플래그.

검증 단위: 문자열 1개(하위 함수) / JD 1건=1행(clean_jd).
"""
import polars as pl

from da_toolkit.module_a.collector import parser
from da_toolkit.module_a.preprocessor import clean
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures" / "manual"


def test_clean_text_strips_html_emoji_whitespace():
    raw = "<p>SQL  &amp;   Python</p>\n\n대시보드 \U0001f600 경험"
    assert clean.clean_text(raw) == "SQL & Python 대시보드 경험"


def test_clean_text_none_passthrough():
    assert clean.clean_text(None) is None
    assert clean.clean_text("   ") is None  # 공백만 남으면 None


def test_normalize_company():
    assert clean.normalize_company("주식회사 토스") == "토스"
    assert clean.normalize_company("우아한형제들(주)") == "우아한형제들"
    assert clean.normalize_company("㈜당근마켓") == "당근마켓"
    assert clean.normalize_company(None) is None


def test_clean_jd_preserves_row_count():
    df = parser.parse_manual_dir(FIXTURES)
    out = clean.clean_jd(df)
    assert out.height == df.height == 5  # 정제는 행을 삭제하지 않는다
    for col in ["company_norm", "text_clean", "too_short"]:
        assert col in out.columns
    assert out["too_short"].dtype == pl.Boolean


def test_too_short_flag_only_not_removed():
    df = pl.DataFrame(
        {
            "company": ["토스", "X"],
            "responsibilities": ["가" * 250, None],
            "requirements": [None, None],
            "preferred": [None, None],
            "body": [None, "짧음"],
        }
    )
    out = clean.clean_jd(df)
    assert out.height == 2  # 짧아도 삭제 안 함
    flags = out["too_short"].to_list()
    assert flags == [False, True]


def test_section_join_fallback_to_body():
    df = pl.DataFrame(
        {
            "company": ["A", "B"],
            "responsibilities": ["주요업무", None],
            "requirements": ["자격요건", None],
            "preferred": [None, None],
            "body": ["본문전체", "폴백본문"],
        }
    )
    out = clean.clean_jd(df)
    texts = out["text_clean"].to_list()
    assert texts[0] == "주요업무 자격요건"  # 섹션 우선 결합
    assert texts[1] == "폴백본문"  # 섹션 전무 → body 폴백
