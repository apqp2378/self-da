"""Module A · Phase 2 전처리 — jd_raw → jd_clean.

스텁. 실제 구현은 Day 10 세션(빌드 가이드 §6)에서 채운다.
정제는 row를 삭제하지 않는다. 200자 미만은 too_short 플래그만 표시 (원칙 5/검증).
"""
from __future__ import annotations


def clean_jd(jd_raw):
    """jd_raw → jd_clean.

    입력 단위: JD 1건 = 1행 (jd_raw)
    출력 단위: JD 1건 = 1행 (jd_clean) — 행 수 불변

    한 책임 한 함수 (원칙 2). HTML 태그·이모지·연속 공백 제거, 회사명 정규화 등은
    하위 함수로 분리하고 여기서 조합한다.
    """
    raise NotImplementedError("Day 10 세션에서 구현")
