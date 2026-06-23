"""Module A · Phase 1 보조 — 자유형식 JD 텍스트 → collector 입력 마크다운(초안).

역할 (CLAUDE.md 원칙 6 준수):
- LLM은 "모호한 자유형식 텍스트를 표준 템플릿으로 구조화/정규화"하는 데만 쓴다.
- required/preferred 최종 분리·tools 추출 같은 결정론적 판단은 하지 않는다.
  그건 collector(섹션 분리)와 skill_extractor(사전 매칭)가 결정론적으로 담당한다.
- 출력은 사람이 검수할 '초안 마크다운'이다. 검수 후 data/raw/manual/에 두면
  parser.py(collector)가 결정론적으로 jd_raw를 만든다.

이 스크립트는 agents/jd_parser.py(LLM이 최종 JSON까지 뽑던 v1)를 대체한다.

사용법:
  python -m da_toolkit.module_a.collector.ingest_llm data/jd/ably.txt \
      --company 에이블리 --posted-date 2026-06-20 \
      --source-url https://example.com/jobs/1 --title "데이터 분석가"
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# LLM은 본문 구조화만. 필수 메타(회사·게시일·URL·직무)는 사람이 인자로 직접 준다(추측 금지).
SYSTEM_PROMPT = """너는 채용공고(JD) 자유 텍스트를 '정해진 마크다운 템플릿'으로 재배치만 한다.

규칙:
- 원문 문구를 보존한다. 요약·창작·추론을 하지 않는다.
- 본문은 정확히 다음 3개 H2 섹션으로 나눈다: '## 주요업무', '## 자격요건', '## 우대사항'.
  원문에 해당 내용이 없으면 그 섹션 헤더만 두고 내용은 비운다.
- frontmatter의 선택 필드(employment_type, experience_level, experience_years, education,
  location, industry, job_category, salary, deadline, team)는 원문에 명시된 것만 채운다.
  명시 안 된 값은 빈 칸으로 둔다.
- 스킬 목록 추출, required/preferred의 최종 판단 같은 분석은 하지 않는다. 너의 일은 '구조화'뿐이다.
- 출력은 마크다운 본문만. 설명·코드블록 표시(```)를 붙이지 않는다."""

OPTIONAL_KEYS = [
    "employment_type", "experience_level", "experience_years", "education",
    "location", "industry", "job_category", "salary", "deadline", "team",
]


def structure_to_markdown(jd_text: str, company: str, posted_date: str,
                          source_url: str, title: str) -> str:
    """자유형식 JD 텍스트 → collector 입력 마크다운(초안) 문자열.

    입력 단위: JD 1건(텍스트)
    출력 단위: JD 1건 = 마크다운 1개 (frontmatter + 3섹션)
    필수 메타는 인자로 받은 값을 그대로 쓴다(LLM이 만지지 않음).
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    user_msg = (
        f"필수 메타(이미 확정, 그대로 frontmatter에 반영):\n"
        f"- company: {company}\n- title: {title}\n"
        f"- posted_date: {posted_date}\n- source_url: {source_url}\n\n"
        f"아래 JD 본문을 템플릿으로 구조화해줘.\n선택 frontmatter 키: {', '.join(OPTIONAL_KEYS)}\n\n"
        f"---\n{jd_text}\n---"
    )
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    body = msg.content[0].text.strip()
    if body.startswith("```"):
        body = body.split("```")[1]
        body = body[4:].strip() if body.startswith("json") else body.strip()
    return body


def main() -> None:
    ap = argparse.ArgumentParser(description="자유형식 JD → collector 입력 마크다운(초안)")
    ap.add_argument("txt_path", help="JD 텍스트 파일 경로 (예: data/jd/ably.txt)")
    ap.add_argument("--company", required=True)
    ap.add_argument("--posted-date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--source-url", required=True)
    ap.add_argument("--title", required=True)
    args = ap.parse_args()

    jd_path = Path(args.txt_path)
    if not jd_path.exists():
        print(f"[오류] 파일 없음: {jd_path}")
        sys.exit(1)

    md = structure_to_markdown(
        jd_path.read_text(encoding="utf-8"),
        args.company, args.posted_date, args.source_url, args.title,
    )

    out_dir = Path("data/raw/manual") / date.today().strftime("%Y%m%d")
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_title = args.title.replace("/", "-").replace(" ", "")
    out_path = out_dir / f"{args.company}_{args.posted_date}_{safe_title}.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"[초안 저장] {out_path}")
    print("→ 본인이 검수한 뒤 parser.py(collector)로 jd_raw를 만드세요 (원칙 6: 분석은 결정론 단계에서).")


if __name__ == "__main__":
    main()
