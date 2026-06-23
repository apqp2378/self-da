# docs/schema.md — Module A 데이터 스키마

> 본 자료는 운영 보조 지표로 활용한다. 분류 정답이 아니다 (원칙 7).

## jd_raw (Phase 1 수집기 출력)

분석 단위: **JD 1건 = 1행**. 출력 파일: `data/interim/jd_raw.parquet`.
원문을 그대로 담는 단계다. 스킬·토픽 등 파이프라인이 계산하는 값은 넣지 않는다.

수집 입력은 `data/raw/manual/YYYYMMDD/{회사}_{게시일}_{직무}.md`.
frontmatter(스칼라 메타) + 본문(고정 헤더 3섹션) 구조.

| 컬럼 | 타입 | 결측 허용 | 출처 | 누수 위험 |
|---|---|---|---|---|
| `jd_id` | str | N | 계산 (dedup_key 앞 12자) | N |
| `company` | str | N | 수집 (frontmatter) | N |
| `title` | str | N | 수집 | N |
| `posted_date` | date | Y | 수집 | N |
| `source_url` | str | Y | 수집 | N |
| `employment_type` | str | Y | 수집 | N |
| `experience_level` | str | Y | 수집 (신입/경력/경력무관) | N |
| `experience_years` | str | Y | 수집 (예: "3년 이상") | N |
| `education` | str | Y | 수집 | N |
| `location` | str | Y | 수집 | N |
| `industry` | str | Y | 수집 (핀테크/이커머스…) | N |
| `job_category` | str | Y | 수집 (공고가 분류한 직군) | N |
| `salary` | str | Y | 수집 | N |
| `deadline` | str | Y | 수집 | N |
| `team` | str | Y | 수집 | N |
| `responsibilities` | str | Y | 수집 (본문 ## 주요업무) | N |
| `requirements` | str | Y | 수집 (본문 ## 자격요건) | N |
| `preferred` | str | Y | 수집 (본문 ## 우대사항) | N |
| `body` | str | Y | 수집 (본문 전체) | N |
| `collected_date` | date | N | 수집 (폴더명 YYYYMMDD) | N |
| `source_file` | str | N | 수집 (파일 경로) | N |
| `dedup_key` | str | N | 계산 (회사+게시일+본문 앞200자 SHA1) | N |
| `is_duplicate` | bool | N | 계산 (dedup_key 첫 등장 외 True, 행 유지) | N |

규칙:
- 결측은 명시적 `None`.
- 중복은 삭제하지 않고 `is_duplicate`로 표시한다.
- 필수 frontmatter(company, title, posted_date, source_url) 누락 또는 파일명 패턴 위반 시 `JDParseError`.

## jd_clean (Phase 2) — Day 10에서 정의
## jd_skill_long (Phase 4) — Day 12에서 정의
