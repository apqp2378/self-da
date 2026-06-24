# docs/self-da-overview.md — self-da 전체 개요 (창작프로젝트 흡수본)

> 2026-06-24 통합 결정: 기존 "창작프로젝트"의 내용은 사실상 self-da(데이터 분석가 취업 4주 계획)였다.
> 프로젝트가 둘로 갈라지면 decision_log·서사가 분산되므로(메모리 "흐름 방지" 원칙),
> 그 계획을 본 문서로 흡수하고 **문제해결 프로젝트를 self-da의 단일 홈**으로 둔다.
> "창작프로젝트"는 더 이상 self-da 작업에 쓰지 않는다(아카이브 권장).

## 한 줄 정의
취업 준비 자체를 DA 프로젝트로 다룬다: 구조적 진단 → 실행 → 산출물. 이 프레이밍이 작업 응집력과 포트폴리오 가치를 만든다.

## 시작 시 진단한 갭
- 이력서·포트폴리오가 특정 회사 맞춤이 아님
- 보여줄 실무 경험 부재
- SQL/Python 코딩테스트 준비 약함
- Claude Skills·MCP 미숙

## 4주 파이프라인
1. Week 1 — JD 수집 + 갭 진단  ← **Module A가 이 단계를 심화** (da_toolkit/module_a/)
2. Week 2 — 모의 48시간 해커톤 (NL→SQL 생성기)
3. Week 3 — 가상 실무 시뮬레이터 (분석 PJT 3개) + CSV→HTML 리포트 빌더 + 블로그 자동화 우회안
4. Week 4 — Streamlit 챗봇 + 포트폴리오 통합

## 현재 상태 (06-23 킥오프 기준)
- GitHub `apqp2378/self-da` 세팅. `git push --rejected`는 `git pull origin main --rebase`로 해결.
- zighang.com에서 JD 5건 수집 → `agents/jd_parser.py`(Claude API)로 구조화 JSON 출력 → `outputs/jd_parsed/`.
- `docs/decision_log.md`에 의사결정 기록(프로젝트 컨셉 근거, 가상 해커톤 프레이밍, 블로그 자동화 Week 3 연기).
- Day 1·2 블로그 초안(Tistory 호환 markdown). Day 3 진행 중(추가 JD 5건 + 첫 Claude Skill 정의).

## 핵심 학습·원칙
- 취업 준비를 DA 프로젝트로 다루는 프레이밍이 전체 응집력의 핵심.
- Tistory Open API는 2024 종료 → 블로그 자동화 비가용, CSV→HTML 빌더로 우회(Week 3).
- 첫 push에서 원격/로컬 분기 시 git rebase 워크플로우 필요.

## 도구
Python · SQL · Git/GitHub · Streamlit · Claude API · Claude Skills/MCP.
플랫폼: GitHub(apqp2378/self-da), Tistory(블로그 기록), zighang.com(JD 소싱).

## 연결
- Module A 배치·결정: 메모리 [[career-ops-module-a-placement]]
- 타깃 직군: 메모리 [[career-north-star]] (이커머스 그로스 분석 1순위)
- 진행 트래커: Notion "Career-Ops Tracker" (JD Inbox / Daily Log / Bullet Bank)
