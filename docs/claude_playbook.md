# Claude 활용 플레이북 — self-da 프로젝트 적용판

**출처 영상** · #4 클로드 완벽 튜토리얼 · #5 상위 1% Claude 활용법 · #6 AI로 상위 1% 되는 법 · #2 Claude 1,000시간 노하우 (#3 16핵=기능 체크리스트, #1 젠슨황=스킵)
**왜 이 문서** · 본인 확인된 퀄리티 문제는 두 가지 — **① 산출물 완성도가 얕다, ② 프로젝트 방향·의사결정이 흐른다.** 둘은 처방이 다르다(§3에서 정조준). 프롬프트 구조(ICC/PRIME)는 보조 도구일 뿐.

> 본 자료는 운영 보조 지표다. 실제 판단·결정은 본인이 한다 (CLAUDE.md 원칙 7).

---

## 1. 사실 vs 의견 (영상 주장 교차검증)

**검증된 사실 (Anthropic 공식 문서로 확인):**
- "Claude를 입사 첫날 신입처럼, 명시적·구체적으로 지시하라" — 공식 가이드의 1번 원칙(Be clear, direct, detailed). 영상들의 ICC/PRIME은 이걸 재포장한 것.
- "예시(few-shot)를 주면 품질이 오른다" — 공식이 "강력 권장"하는 best practice. 영상 #5의 E(Examples)와 일치.
- 2026 현재: **Cowork**(에이전트형, 유료 데스크톱), **Skills**(반복 작업 패키지, Anthropic제+커스텀), **Connectors**(Drive/Gmail/Calendar/GitHub/Slack 등), **Plan mode**, **Claude Code** 모두 실제 제공. 모델은 Opus(복잡/빌드)·Sonnet(기본)·Haiku(빠름/대량).

**화자 의견·경험 (표본=화자 본인, 일반화 주의):**
- "3회/주 이상이면 무조건 스킬화", "10-80-10", "6레벨" — 유용한 휴리스틱이나 화자 개인 운영 규칙. 절대 기준 아님.
- "이메일은 손대지 마라, 다 AI에게" — 화자(사업가) 맥락. 신입 취준 맥락엔 그대로 적용 안 됨.

**과장 의심:**
- 영상 다수가 자기 유료 상품(Apex, AI OS playbook, Hexfield 등) 홍보가 섞임 — 프레임워크만 취하고 제품 권유는 버린다.

---

## 2. 핵심 프레임워크 — self-da 작업에 적용

### 2-1. ICC (프롬프트 1건 단위)
**I**nstruction(할 일) · **C**ontext(역할·배경·파일) · **C**onstraint(규칙·형식·길이) + **Example**(좋은 출력 1개).
- 나쁨: "토픽 라벨 좀 붙여줘" → 일반적 결과
- 좋음: "[I] 아래 BERTopic 토픽 5개에 사람이 읽을 라벨 후보 3개씩 제안 / [C] 나는 DA 취준생, 토픽은 채용공고 분류용, docs/domain_taxonomy.md 매핑 참고 / [C] 표로, unknown 허용, 최종 결정은 내가 함 / [예] '이커머스 그로스 분석'처럼"

### 2-2. PRIME (작업 1건 단위, ICC 확장)
**P**urpose(진짜 목적) · **R**esearch(자료·검증) · **I**nterview(답변 전 나에게 질문) · **M**echanics(출력 형태) · **E**xample.
- 핵심 습관 두 개: **① 컨텍스트 인터뷰** = 프롬프트 끝에 "답하기 전에 필요한 정보를 나에게 물어봐" / **② Ground first, ask second** = "먼저 X를 리서치·검증해" 한 번 돌린 뒤 본 작업 요청. (이 두 개가 퀄리티 레버 1순위)

### 2-3. Game Matrix — 내 작업을 4분면으로
| 분면 | 기준 | self-da 작업 예시 |
|---|---|---|
| **Give**(AI에 위임) | 쉽고·반복·규칙적 | JD 파싱(parser.py), 스킬 빈도 집계, EDA 차트, 마크다운 변환, 커밋 메시지 |
| **Accelerate**(AI 가속) | 사람엔 오래·AI엔 쉬움 | 토픽 후보 압축, 도메인 리서치, 이력서 갭 분석, 면접 예상질문 |
| **Integrate**(사람이 디렉팅) | 둘 다 어려움·taste 필요 | 토픽 라벨 최종 확정, Bullet 과장위험 판단, 직군 타겟 결정, 포트폴리오 서사 |
| **No-AI**(사람만) | 인간성·관계 | 실제 면접, 네트워킹, 본인 강점·지향 결정 |

> 이 분면은 CLAUDE.md 원칙 6(결정론=AI, 판단=사람)·원칙 7과 정확히 일치한다. Give=결정론 코드, Integrate=사람 검수.

### 2-4. Rule of Rs — 스킬화 판단
**R**epetitive(주1회+) · **R**ules-based(입출력 동일) · **R**eturn(만드는 시간 < 아끼는 시간). 셋 다 Yes면 스킬/스케줄화.

---

## 3. 본인 적용 — 확인된 두 문제 정조준

### 문제 ① 산출물 완성도가 얕다
근본 처방은 프롬프트가 아니라 **완성 기준 + 이터레이션**이다.
- **"완성도 기준(Definition of Done)"을 작업 전에 못박는다.** 예: 분석 노트는 "문제정의→데이터→EDA→해석→비즈니스 제언→한계" 6칸이 다 차야 완성(합격포폴 가이드 기준). 코드는 "테스트 통과 + docstring 단위 명시"가 완성. 기준 없이 시작하니 얕은 데서 멈춘다.
- **예시(Example)를 먼저 준다.** "좋은 산출물 1개"를 붙이면 깊이가 그 수준으로 맞춰진다(공식 가이드: few-shot이 품질 최대 레버).
- **10-80-10:** 첫 출력에서 멈추지 말 것. AI 80% 초안 → 본인이 마지막 10%(깊이·디테일·본인 사례)를 직접 채운다. 한 방을 기대하면 얕게 끝난다.
- **자기검증 루프(템플릿 C)를 매 산출물에 적용.** "약한 부분·빠진 관점·과장 표시" → 다시 채움. 영상 #2·#5의 critique 습관.

### 문제 ② 방향·의사결정이 흐른다
이건 **AI에 위임하면 안 되는 영역**이다(Game Matrix: Integrate/No-AI = taste·vision·sequencing은 사람 몫). AI는 옵션만, 결정은 본인.
- **North Star 한 줄을 고정한다.** "나는 어느 직군 결(이커머스 그로스 / 마케팅분석 / 플랫폼BI …)을 노리는가"를 먼저 정하면 Module A·이력서·면접이 한 방향으로 정렬된다. 안 정하면 매 산출물이 따로 논다.
- **성공 기준 기반 실행(원칙 4).** 작업마다 "이게 되면 끝"을 한 줄로 적고 시작. "버그 고쳐줘"가 아니라 "재현 테스트 통과시켜줘".
- **결정엔 plan mode / 옵션 비교를 쓴다.** AI에게 "결정해줘"가 아니라 "선택지 3개와 트레이드오프를 표로" → 본인이 고른다. (이번 세션의 self-da 흡수·JD 파서 통합 결정이 그 방식)
- **결정은 decision_log.md(D-00x)에 기록.** 흐름 방지의 핵심은 "왜 그렇게 정했는지"를 남기는 것.

### 반복 작업 → 스킬/스케줄 (Rule of Rs 통과)
- JD 등록(#1) → 커스텀 스킬 후보 · 주간 Bullet 추출(#3) → 스킬 후보
- Daily Log 기록(#2) → **스케줄 태스크 설정 완료**(매일 21시 자동 초안)
- (보유) youtube-script-to-learning-note ✓
- **모델:** 기본 Sonnet, 코드·설계 빌드 시 Opus, 대량 단순 요약은 Haiku.

---

## 4. 반복용 프롬프트 템플릿 (복붙·빈칸 채우기 — "스킬화"의 핵심)

### 템플릿 A — ICC 작업 요청
```
[Instruction] 무엇을 해줘:
[Context] 나는 DA 취준생, 프로젝트는 self-da/Module A. 참고 파일:
[Constraint] 규칙·형식·길이 / unknown 허용 / 최종 결정은 내가 함:
[Example] 좋은 출력 1개:
답하기 전에, 더 필요한 정보가 있으면 나에게 먼저 물어봐.
```

### 템플릿 B — PRIME 심층 작업 (이력서·면접·전략)
```
[Purpose] 이 작업의 진짜 목적/원하는 결과:
[Research] 먼저 ___를 리서치·검증해. 출처는 공식 문서 우선, 지어내지 마.
[Interview] 답하기 전에 나에게 객관식으로 3개 질문해.
[Mechanics] 출력 형태(표/문단/길이/톤):
[Example] 참고할 좋은 예시:
```

### 템플릿 C — 자기검증 (출력 직후 붙이기)
```
방금 결과를 비판적으로 검수해. 약한 부분·빠진 가정·과장된 표현·검증 안 된 수치를 표시하고, 근거 있는 것만 남겨. (CLAUDE.md 원칙 4)
```

> **스킬로 등록하려면:** 위 템플릿들을 Settings → Capabilities → Skills에서 커스텀 스킬로 저장하면 매번 자동 호출된다. (이 세션에서 스킬 생성은 불가 — 본인이 등록)

---

## 5. 포트폴리오·면접 연결 (STAR)

- **S:** DA 취업 준비를 데이터 방식으로 자동화하는 self-da 프로젝트 운영 중, AI 활용 품질이 들쭉날쭉했다.
- **T:** Claude를 일관된 품질로 쓰도록 작업 설계 표준을 만들 필요.
- **A:** 파워유저 사례를 ICC/PRIME/Game Matrix로 정리하고, 결정론 작업(Give)과 사람 판단(Integrate)을 분리하는 원칙(CLAUDE.md 원칙 6·7)에 매핑했다. 반복 작업은 Rule of Rs로 스킬·스케줄화.
- **R:** (예상/정량) 토픽 라벨링·Bullet 추출 재작업률 감소, 주간 운영 시간 단축 — 적용 후 측정 예정.
- **면접 1문장:** "AI를 '도구 나열'이 아니라 작업 분배 프레임워크로 표준화해, 결정론 작업과 사람 판단을 분리하고 반복 작업을 자동화했습니다." (현재 검토·적용 단계로 정직하게 표현)

---

## 출처
- Anthropic, Be clear, direct, and detailed — https://docs.anthropic.com/en/docs/be-clear-direct
- Anthropic, Prompt engineering overview — https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- Anthropic, Use multiple examples (multishot) — https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting
- Anthropic, Claude Cowork — https://www.anthropic.com/product/claude-cowork
- Claude Help Center, What are skills? — https://support.claude.com/en/articles/12512176-what-are-skills
