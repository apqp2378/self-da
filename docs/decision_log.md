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
