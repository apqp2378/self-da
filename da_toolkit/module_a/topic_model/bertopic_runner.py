"""Module A · Phase 3 토픽 분류 — jd_clean → 토픽.

스텁. 실제 구현은 Day 11 세션(빌드 가이드 §7)에서 채운다.
- BERTopic 학습 자체에 LLM 호출하지 않는다 (원칙 6). LLM은 라벨링 검수에만.
- outlier(-1)를 강제로 제거하지 않는다. 분류 못 한 JD는 unknown으로 둔다 (원칙 7).
- random_state 고정 (재현성).
"""
from __future__ import annotations


def fit_topics(jd_clean, embedding_model: str, random_state: int = 42):
    """jd_clean → 토픽 배정 + 토픽 메타.

    입력 단위: JD 1건 = 1행 (too_short 제외)
    출력 단위:
        (1) JD 1건 = 1행 + topic_id  (배정)
        (2) 토픽 1개 = 1행 + 대표 키워드 10개 / 대표 JD 3건 / 토픽 크기

    min_topic_size 권장: JD 수의 5~10%. 토픽 수 현실 범위 3~7개.
    """
    raise NotImplementedError("Day 11 세션에서 구현")
