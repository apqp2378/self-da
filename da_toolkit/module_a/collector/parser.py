"""Module A · Phase 1 수집기 — 수동 수집 마크다운 → jd_raw.

스텁. 실제 구현은 Day 9 세션(빌드 가이드 §5)에서 채운다.
구현 전 docs/schema.md의 jd_raw 컬럼 정의를 먼저 확정할 것 (원칙 1).
외부 라이브러리는 frontmatter 파싱에 python-frontmatter, 데이터 처리에 polars만 사용 (§5.3).
"""
from __future__ import annotations


def parse_manual_jd(input_dir: str):
    """수동 수집 마크다운 폴더 → jd_raw.

    입력 단위: data/raw/manual/YYYYMMDD/{회사}_{게시일}_{직무}.md 1파일 = JD 1건
    출력 단위: JD 1건 = 1행 (jd_raw)

    원칙 5: 입력·출력 단위를 혼동하지 않는다.
    중복 감지는 회사명 + 게시일 + 본문 앞 200자 해시 기준 (§5.2).
    """
    raise NotImplementedError("Day 9 세션에서 구현")
