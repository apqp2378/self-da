# Module A — 채용공고 토픽 분류기

self-da **Week 1(진단·정의)의 JD Parser → Gap Matcher를 심화**하는 모듈.
DA 채용공고를 BERTopic으로 토픽 분류하고 토픽별 스킬 빈도표를 산출한다.
산출물은 Module B(역량 갭 점수)의 입력이 된다.

## JD 처리 2단계 (원칙 6: LLM ↔ 결정론 분리, D-004)

1. `collector/ingest_llm.py` — (선택) LLM이 자유형식 JD 텍스트를 표준 마크다운 템플릿으로 **구조화만** 한다. 필수 메타는 사람이 인자로 제공. 출력은 검수용 초안.
2. `collector/parser.py` — 마크다운 → `jd_raw`를 **결정론적**으로 생성(섹션 분리·중복 표시).

> 기존 `agents/jd_parser.py`(LLM이 최종 JSON까지 추출)는 v1로 대체(deprecated). 결과 5건은 `data/raw/manual/_migrated_20260623/`에 마크다운으로 이관됨.

## 상태

| 단계 | 파일 | 세션 |
|---|---|---|
| 수집(구조화·선택) | `collector/ingest_llm.py` | — |
| 수집(jd_raw) | `collector/parser.py` | Day 9 (§5) ✓ |
| 전처리 | `preprocessor/clean.py` | Day 10 (§6) |
| 토픽 | `topic_model/bertopic_runner.py` | Day 11 (§7) |
| 스킬 | `skill_extractor/extractor.py`, `skill_dict.yaml` | Day 12 (§8) |

> 본 모듈의 모든 산출물은 운영 보조 지표다. 분류 정답이 아니다 (원칙 7).
