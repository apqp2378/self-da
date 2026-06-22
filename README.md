# Self-DA · 데이터 분석 직무 취업 준비 자동화 시스템

> 채용공고와 나 사이의 Gap을 정량적으로 측정하고, 30일 안에 Gap을 줄이는 학습·산출물 생성 파이프라인을 자동화합니다.

## 🎯 문제 정의

데이터 분석 직무 취업 준비 과정에서 다음 4가지 부족함을 정의했습니다:

1. **이력서·포트폴리오** — 회사별 요구 역량에 맞춘 맞춤화 부재
2. **실무 경험** — 분석 의뢰 → 보고서 작성 사이클 경험 부족
3. **코딩 테스트** — SQL·Python 약점 토픽 미파악, 반복 실수 패턴 미정리
4. **Claude Skill·MCP** — AI 도구를 워크플로우에 구조화한 경험 부족

각각을 측정 가능한 지표로 정의하고, Claude 기반 자동화로 해결합니다.

## 🛠️ 시스템 구조
[채용공고]  →  [JD Parser]  →  [Gap Matrix]  →  [Solver Agents]  →  [산출물]
├─ NL→SQL 생성기 (코딩테스트)
├─ Mock PM Bot (가상 실무)
└─ Resume Patcher (이력서)

## 📦 핵심 산출물

| 산출물 | 설명 | 위치 |
|---|---|---|
| `da_toolkit/nl2sql/` | 자연어→SQL 생성기 (가상 해커톤 48h 산출물) | Week 2 |
| `da_toolkit/csv2html/` | CSV→HTML 인사이트 리포트 빌더 | Week 3 |
| `da_toolkit/streamlit_chatbot/` | Streamlit DA 챗봇 (통합 인터페이스) | Week 4 |
| `notebooks/p{1,2,3}_*.ipynb` | 가상 분석 프로젝트 3건 | Week 3 |
| `outputs/resume/` | 회사별 맞춤 이력서 5종 | Week 4 |

## 📊 측정 지표

| 지표 | 시작값 | 목표값 (Day 30) |
|---|---|---|
| JD 매칭 점수 평균 | TBD | +20%p |
| SQL 약점 토픽 정답률 | TBD | 60% 이상 |
| 면접 답변 가능 프로젝트 수 | 0~1개 | 4개 |
| 회사 맞춤 이력서 변형본 | 0개 | 5개 |

## 🗓️ 진행 상황

전체 로드맵: [ROADMAP.md](./ROADMAP.md)

- [x] Day 0 (6/23) · 사전 준비
- [ ] Day 1~7 · 진단·정의
- [ ] Day 8~14 · 가상 해커톤 + NL→SQL
- [ ] Day 15~21 · 가상 실무 시뮬레이터
- [ ] Day 22~30 · 통합·포트폴리오화

## 🔗 관련 프로젝트

- [reward-ad-performance-analysis](https://github.com/apqp2378/reward-ad-performance-analysis) — 광고 성과 분석
- [lithium-battery-rul-analysis](https://github.com/apqp2378/lithium-battery-rul-analysis) — NASA 배터리 RUL 분석
- [lendingclub-default-risk-analysis](https://github.com/apqp2378/lendingclub-default-risk-analysis) — 대출 리스크 분석

## 📝 의사결정 로그

주요 설계 결정과 그 근거: [docs/decision_log.md](./docs/decision_log.md)
