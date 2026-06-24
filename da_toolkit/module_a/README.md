# Module A — 채용공고 분류기 + 스킬 빈도

self-da **Week 1(진단·정의)의 JD Parser → Gap Matcher를 심화**하는 모듈.
DA 채용공고를 `docs/domain_taxonomy.md` 라벨로 **규칙 기반 분류**하고 라벨별 스킬 빈도표를 산출한다.
산출물은 Module B(역량 갭 점수)의 입력이 된다.

## 분류 방식 결정 (2026-06-24)
토픽 축은 **BERTopic(비지도)이 아니라 규칙 기반 분류**로 간다.
- 근거: JD 코퍼스가 작고(수십~수백 건) 동질적이라 UMAP+HDBSCAN 클러스터가 불안정·outlier 과다.
  또한 라벨 후보(이커머스 그로스 / 마케팅·캠페인 / 플랫폼BI / 스타트업 제너럴 / 인하우스 리서치)가
  `domain_taxonomy.md`에 이미 정의돼 있어 "발견"이 아니라 "매핑" 문제다.
- BERTopic은 폐기하지 않고 **일회성 검증(EDA)으로 강등**: 규칙 라벨과 비지도 클러스터의 일치도를
  점검하고 그 근거를 decision_log에 남긴다(포트폴리오·면접 서사용). 파이프라인 의존성은 아니다.

## 상태
스캐폴드 생성됨. 각 단계는 빌드 가이드 일정에 따라 채운다.

| 단계 | 파일 | 세션 | 상태 |
|---|---|---|---|
| 수집 | `collector/parser.py` | Day 9 (§5) | ✅ 완료 |
| 전처리 | `preprocessor/clean.py` | Day 10 (§6) | 🔨 진행 |
| 분류(규칙) | `classifier/rule_classify.py`, `label_rules.yaml` | Day 11 (§7 개정) | ⬜ 예정 |
| 스킬 | `skill_extractor/extractor.py`, `skill_dict.yaml` | Day 12 (§8) | ⬜ 예정 |
| 검증(선택) | `topic_model/bertopic_runner.py` (BERTopic 일치도 EDA) | Day 13/여유 시 | ⬜ 강등 |

> 본 모듈의 모든 산출물은 운영 보조 지표다. 분류 정답이 아니다 (원칙 7).
