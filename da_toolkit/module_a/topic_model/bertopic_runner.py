"""Module A · 검증(EDA) — BERTopic 일치도 점검. (파이프라인 단계 아님)

[강등 2026-06-24] 파이프라인 토픽 축은 classifier/rule_classify.py(규칙 기반)로 간다.
이 파일은 폐기하지 않고 **일회성 검증 도구**로 남긴다:
규칙 라벨과 BERTopic 비지도 클러스터의 일치도를 점검하고 그 근거를 decision_log에 기록한다
(포트폴리오·면접 서사용). Module B 입력은 규칙 라벨이며 이 모듈에 의존하지 않는다.

스텁. 구현은 분류 라벨이 나온 뒤 Day 13/여유 시 진행한다.
- BERTopic 학습 자체에 LLM 호출하지 않는다 (원칙 6). LLM은 라벨링 검수에만.
- outlier(-1)를 강제로 제거하지 않는다 (원칙 7).
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
