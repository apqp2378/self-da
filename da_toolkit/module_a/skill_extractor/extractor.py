"""Module A · Phase 4 스킬 추출 — jd_clean + skill_dict → jd_skill_long.

스텁. 실제 구현은 Day 12 세션(빌드 가이드 §8)에서 채운다.
스킬 매칭은 정규식 + 사전 기반. LLM 호출 안 함 (원칙 6).
단, '우대: 대시보드 경험' 같은 모호한 표현 정규화만 LLM 예외 허용.
"""
from __future__ import annotations


def extract_skills(jd_clean, skill_dict: dict):
    """jd_clean → jd_skill_long.

    입력 단위: JD 1건 = 1행
    출력 단위: JD 1건 × 스킬 1건 = 1행 (long format)

    사전에 없는 단어는 unknown_terms.csv로 따로 저장 → 본인 검토 후 사전 보강 루프.
    """
    raise NotImplementedError("Day 12 세션에서 구현")


def aggregate_skills_by_topic(jd_skill_long, topic_map):
    """jd_skill_long → skill_demand_by_topic.

    입력 단위: JD 1건 × 스킬 1건 = 1행 (long format)
    출력 단위: 토픽 1개 × 스킬 1건 = 1행 (long format)
    """
    raise NotImplementedError("Day 12 세션에서 구현")
