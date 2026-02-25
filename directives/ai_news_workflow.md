# AI 뉴스 자동화 워크플로우 지침 (AI News Workflow Directive)

이 문서는 AI 뉴스 수집 및 처리 시스템의 운영 절차를 정의합니다.

## 목표
- `RSSList.json`에 등록된 주요 AI 뉴스 소스로부터 최신 트렌드를 자동으로 수집합니다.
- 수집된 내용을 제텔카스텐 스타일의 영구 노트로 변환하여 지식 자산화합니다.

## 워크플로우 실행 방법

가장 간편한 방법은 루트 디렉토리에서 통합 실행 스크립트를 사용하는 것입니다:

```bash
# 한 번에 수집부터 처리까지 실행
./run.sh
# 또는
python3 main.py
```

## 상세 워크플로우 단계

### 1. 뉴스 수집 및 필터링 (Execution Layer)
- **도구**: `execution/fetch_rss.py`
- **입력**: `RSSList.json`
- **규칙**:
  - 각 소스당 최대 5개의 게시물을 가져옴.
  - 현재 시간 기준 24시간 이내의 게시물만 필터링.
- **출력**: `.tmp/latest_news.json`

### 2. 콘텐츠 요약 및 포맷팅 (Orchestration & Execution Layer)
- **도구**: `execution/process_content.py`
- **입력**: `.tmp/latest_news.json`, `makeMD.md` (프롬프트 지침)
- **처리**:
  - LLM을 사용하여 한국어 제목, 인사이트, 주요 내용, 파인만 식 설명을 생성.
- **출력**: `news/` 폴더에 Markdown 파일 생성.

### 3. 파일 저장 규칙
- **디렉토리**: `news/`
- **파일명**: `YYYY-MM-DD-키워드-해시.md`
  - 예: `2024-05-21-gpt4-multimodal-a3f9c2e1.md`
- **해시값**: URL 기준 SHA-256 해시의 앞 8자리 사용.

## 예외 처리 및 학습 (Self-annealing)
- RSS 피드 형식이 변경되어 파싱에 실패할 경우 스크립트를 업데이트하고 본 지침을 보완합니다.
- LLM API 할당량 초과 시 재시도 로직을 구현하거나 사용자에게 알립니다.
