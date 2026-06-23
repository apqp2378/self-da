"""parser.py 검증 — 샘플 5건 통과 + 규칙 위반 에러.

검증 단위: 폴더(JD 5건) 1회 파싱 결과를 단언.
"""
from pathlib import Path

import polars as pl
import pytest

from da_toolkit.module_a.collector import parser

FIXTURES = Path(__file__).parent / "fixtures" / "manual"


def test_parse_five_samples():
    df = parser.parse_manual_dir(FIXTURES)
    assert df.height == 5
    for col in parser.JD_RAW_SCHEMA:
        assert col in df.columns
    for col in ["jd_id", "company", "title", "posted_date", "source_url", "dedup_key", "collected_date"]:
        assert df[col].null_count() == 0, f"{col} 결측 발생"


def test_duplicate_flagged_not_removed():
    df = parser.parse_manual_dir(FIXTURES)
    assert df.height == 5  # 정제는 row를 삭제하지 않는다
    assert int(df["is_duplicate"].sum()) == 1


def test_optional_missing_is_none():
    df = parser.parse_manual_dir(FIXTURES)
    row = df.filter(pl.col("company") == "당근마켓").row(0, named=True)
    assert row["experience_years"] is None
    assert row["preferred"] is None  # 우대사항 섹션 없음
    assert row["requirements"] is not None


def test_sections_split():
    df = parser.parse_manual_dir(FIXTURES)
    row = df.filter(pl.col("company") == "토스").row(0, named=True)
    assert "대시보드" in row["responsibilities"]
    assert "SQL" in row["requirements"]
    assert row["preferred"] is not None


def test_filename_violation(tmp_path):
    d = tmp_path / "20260620"
    d.mkdir()
    (d / "badname.md").write_text(
        "---\ncompany: X\ntitle: Y\nposted_date: 2026-06-20\nsource_url: http://x\n---\n## 자격요건\n- a",
        encoding="utf-8",
    )
    with pytest.raises(parser.JDParseError):
        parser.parse_manual_dir(tmp_path)


def test_missing_required_frontmatter(tmp_path):
    d = tmp_path / "20260620"
    d.mkdir()
    (d / "회사_2026-06-20_직무.md").write_text(
        "---\ncompany: 회사\ntitle: 직무\n---\n## 자격요건\n- a",
        encoding="utf-8",
    )
    with pytest.raises(parser.JDParseError):
        parser.parse_manual_dir(tmp_path)
