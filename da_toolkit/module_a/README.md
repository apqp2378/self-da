# Module A — 채용공고 토픽 분류기

self-da **Week 1(진단·정의)의 JD Parser → Gap Matcher를 심화**하는 모듈.
DA 채용공고를 BERTopic으로 토픽 분류하고 토픽별 스킬 빈도표를 산출한다.
산출물은 Module B(역량 갭 점수)의 입력이 된다.

## 상태
스캐폴드만 생성됨. 각 단계는 빌드 가이드 일정에 따라 채운다.

| 단계 | 파일 | 세션 |
|---|---|---|
| 수집 | `collector/parser.py` | Day 9 (§5) |
| 전처리 | `preprocessor/clean.py` | Day 10 (§6) |
| 토픽 | `topic_model/bertopic_runner.py` | Day 11 (§7) |
| 스킬 | `skill_extractor/extractor.py`, `skill_dict.yaml` | Day 12 (§8) |

> 본 모듈의 모든 산출물은 운영 보조 지표다. 분류 정답이 아니다 (원칙 7).
