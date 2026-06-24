# 의사결정 로그

## 2026-06-23 · Day 0

### D-001 · 프로젝트 컨셉
- 결정: 자기 약점을 DA 방식으로 측정·자동화하는 메타 프로젝트
- 근거: 분석 프로젝트 3개는 이미 있음. 차별화는 자기주도성·도구 활용

### D-002 · 가상 해커톤
- 결정: 7/1~7/2 48h 챌린지, NL→SQL MVP 완성
- 근거: 실제 해커톤 미참가를 코드+데모+회고 글 3종으로 보완

### D-003 · 블로그 초안 생성기 배치 시점
- 결정: Week 3에서 CSV→HTML 리포트 빌더와 함께 구현
- 대안: Day 1 시점에 간단 버전 / 수동 운영
- 근거: 둘 다 "데이터 → 정형 문서 자동 생성" 계열이라 코드 재사용 + 면접 스토리 일관성 확보. 티스토리 Open API는 2024년 종료되어 발행 자동화는 불가, 초안 생성까지만 자동화(반자동)
- 트레이드오프: Week 3까지 블로그는 수동 작성 → 대신 그 수동 경험이 자동화 설계의 요구사항이 됨

### D-004 · JD 파서 2단계 역할분리 (LLM ↔ 결정론)
- 결정: JD 처리를 2단계로 분리한다.
  1) `da_toolkit/module_a/collector/ingest_llm.py` — LLM은 자유형식 JD 텍스트를 표준 마크다운 템플릿으로 **구조화만** 한다(필수 메타는 사람이 인자로 직접 제공).
  2) `da_toolkit/module_a/collector/parser.py` — 마크다운 → `jd_raw`를 **결정론적**으로 생성(섹션 분리·중복 표시). 스킬 추출은 `skill_extractor`(사전+정규식)가 담당.
- 대안: 기존 `agents/jd_parser.py`(LLM이 최종 JSON까지 추출) 단일 유지.
- 근거: 기존 방식은 required/preferred 분리·tools 추출을 LLM이 해서 **원칙 6(결정론 작업에 LLM 금지) 위반**이고, 실제로 `tools:[]` 누락 등 불안정. 2단계로 LLM 역할을 '구조화/정규화'로 좁히면 원칙 6을 지키면서 자유 텍스트 입력 편의도 유지된다.
- 후속: `agents/jd_parser.py`는 v1로 **대체(deprecated)**. 기존 `outputs/jd_parsed/*.json` 5건은 `data/raw/manual/_migrated_20260623/`에 마크다운으로 이관(posted_date·source_url은 본인 보완 후 collector 투입).

### D-005 · North Star 직군 결 확정
- 결정: 타깃 직군 1순위 **이커머스 그로스 분석**, 보조 **마케팅분석**, 안전망 **스타트업 제너럴리스트**.
- 근거: ① 본인 성향=비즈니스·설득(지표 해석·가설 제안 선호) ② 자산 매칭=리워드광고 그로스 분석 PJT가 직접 연결 ③ 수집 JD가 이미 이커머스·O2O 그로스 쪽(ably·patalab 등) ④ 신입 채용 문이 상대적으로 넓음.
- 모델링 자산(배터리RUL·LendingClub)은 메인 아님 → "정량·모델링도 가능" 보강 카드로 활용. 인하우스리서치는 신입 진입 좁아 보조.
- 정렬 효과(이 결정이 바꾸는 것):
  - Module A: 토픽 라벨·스킬 빈도 해석을 이커머스/그로스 중심으로 우선.
  - JD 수집: 이커머스·커머스·O2O 그로스 공고 우선 수집.
  - 이력서: 리워드광고 그로스 분석을 헤드라인으로, 배터리·LendingClub은 모델링 보강.
  - Bullet Bank `직군 적합도`: 이커머스·마케팅분석 태그 우선.

## D-006 — Module A 토픽 엔진: BERTopic → 규칙 기반 분류 (2026-06-24)
- 결정: 토픽 축을 BERTopic(비지도) → 규칙 기반 분류(classifier/rule_classify.py + label_rules.yaml)로 전환.
  BERTopic(bertopic_runner.py)은 폐기하지 않고 규칙 라벨 vs 비지도 클러스터 "일치도 검증(EDA)"용으로 강등.
- 근거: JD 코퍼스가 작고(수십~수백) 동질적 → UMAP+HDBSCAN 클러스터 불안정·outlier 과다.
  라벨 후보가 domain_taxonomy.md에 이미 정의됨 → "발견"이 아니라 "매핑" 문제.
  결정론적·설명가능·표본 안정적. 원칙 6(결정론 작업에 LLM 미사용)과 정렬.
- 영향: skill_extractor 집계 축을 topic_map → rule label(jd_label)로 변경(Day 12). Module B 입력은 규칙 라벨.
- 출처: 리워드광고 PJT의 "규칙 + BERTopic 캐스케이드" 패턴 재사용.