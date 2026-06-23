"""
JD Parser Agent v1
채용공고(JD) 텍스트를 입력받아 구조화된 JSON으로 변환한다.

출력 스키마:
{
  "company": 회사명,
  "position": 직무명,
  "required": [필수 자격요건 리스트],
  "preferred": [우대사항 리스트],
  "tools": [언급된 도구·기술 리스트],
  "domain": [도메인 리스트],
  "experience": 경력 요건
}

사용법:
  python agents/jd_parser.py data/jd/ably_da_intern.txt
"""

import os
import sys
import json
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

# .env에서 API 키 로드
load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# JD에서 추출할 항목을 정의한 시스템 프롬프트
SYSTEM_PROMPT = """당신은 채용공고(JD)를 분석해 구조화하는 전문가입니다.
주어진 JD 텍스트에서 아래 항목을 추출해 JSON으로만 응답하세요.
설명, 마크다운 코드블록(```), 그 외 어떤 텍스트도 붙이지 마세요. 오직 JSON만 출력합니다.

추출 항목:
- company: 회사명 (문자열)
- position: 직무명 (문자열)
- required: 필수 자격요건 (문자열 배열). 명시된 것만. 없으면 빈 배열.
- preferred: 우대사항 (문자열 배열). 없으면 빈 배열.
- tools: 언급된 도구·기술·언어 (문자열 배열). 예: SQL, Python, Tableau, GA4
- domain: 비즈니스 도메인 (문자열 배열). 예: 이커머스, 광고, 핀테크
- experience: 경력 요건 (문자열). 예: "신입", "3년 이하", "경력무관"

각 항목은 JD에 실제로 적힌 내용만 반영하고, 추측해서 채우지 마세요.
required와 preferred를 구분하기 어려우면, '필수/자격요건'으로 표현된 것은 required,
'우대/있으면 좋은'으로 표현된 것은 preferred로 분류하세요."""


def parse_jd(jd_text: str) -> dict:
    """JD 텍스트를 받아 구조화된 dict를 반환한다."""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"다음 JD를 분석해 JSON으로 출력하세요:\n\n{jd_text}"}
        ],
    )

    # 응답 텍스트 추출
    raw = message.content[0].text.strip()

    # 혹시 코드블록이 붙어있으면 제거 (안전장치)
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    # JSON 파싱
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[오류] JSON 파싱 실패: {e}")
        print(f"[원본 응답]\n{raw}")
        sys.exit(1)


def main():
    # 커맨드라인 인자로 JD 파일 경로 받기
    if len(sys.argv) < 2:
        print("사용법: python agents/jd_parser.py <JD파일경로>")
        print("예시:   python agents/jd_parser.py data/jd/ably_da_intern.txt")
        sys.exit(1)

    jd_path = Path(sys.argv[1])

    if not jd_path.exists():
        print(f"[오류] 파일을 찾을 수 없습니다: {jd_path}")
        sys.exit(1)

    # JD 텍스트 읽기
    jd_text = jd_path.read_text(encoding="utf-8")
    print(f"[입력] {jd_path.name} ({len(jd_text)}자) 분석 중...\n")

    # 파싱
    result = parse_jd(jd_text)

    # 결과를 화면에 보기 좋게 출력
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # outputs/jd_parsed/ 에 저장
    out_dir = Path("outputs/jd_parsed")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{jd_path.stem}.json"
    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n[저장] {out_path}")


if __name__ == "__main__":
    main()