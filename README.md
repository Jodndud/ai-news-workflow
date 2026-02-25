# AI News Workflow (AI 뉴스 자동화 워크플로우)

AI 뉴스 RSS 피드를 수집하고, Google Gemini API를 사용하여 요약 및 분석한 뒤, GitHub 저장소로 자동 동기화하는 자동화 도구입니다.

## 🚀 주요 기능
- **뉴스 수집**: 설정된 RSS 피드에서 최신 기술 및 AI 관련 뉴스를 자동으로 가져옵니다.
- **AI 요약 및 분석**: Google Gemini API를 활용하여 뉴스를 한 줄 요약, 주요 포인트, 인사이트 등으로 정리합니다.
- **GitHub 동기화**: 생성된 마크다운(Markdown) 파일을 지정된 로컬 GitHub 저장소 경로로 복사하고, 자동으로 커밋 및 푸시합니다.

---

## 🛠️ 설정 및 설치 방법

### 1. 사전 요구 사항
- **Python 3.x**: 시스템에 설치되어 있어야 합니다.
- **Git**: GitHub 연동을 위해 필요합니다.
- **Google API Key**: Gemini Pro 모델 사용을 위해 [Google AI Studio](https://aistudio.google.com/)에서 API 키를 발급받으세요.

### 2. 의존성 설치
터미널에서 프로젝트 루트 디렉토리로 이동한 후 다음 명령어를 실행하여 필요한 패키지를 설치합니다.
```bash
pip install feedparser python-dotenv google-generativeai
```

### 3. 환경 변수 설정
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 내용을 수정합니다.
```bash
cp .env.example .env
```
`.env` 파일 내용 예시:
```env
# Google Gemini API 키
GOOGLE_API_KEY=your_actual_google_api_key_here

# GitHub 저장소 로컬 경로 (동기화 대상 저장소의 절대 경로)
AMUZ_MEMO_PATH=/Users/username/Project/amuz-memo
```

---

## 📖 사용 방법

### 전체 워크플로우 실행
프로젝트 루트에 있는 `run.sh` 또는 `main.py`를 실행하면 모든 단계(수집 -> 요약 -> 동기화)가 순차적으로 진행됩니다.

**방법 1: 쉘 스크립트 실행 (권장)**
```bash
chmod +x run.sh
./run.sh
```

**방법 2: 파이썬 직접 실행**
```bash
python3 main.py
```

---

## 🔧 주요 코드 수정 및 커스텀 가이드

### 뉴스 소스 수정 (`RSSList.json`)
수집하려는 RSS 피드 주소나 카테고리를 변경하려면 이 파일을 수정하세요.
```json
{
  "IT/AI": [
    "https://example.com/rss",
    ...
  ]
}
```

### 요약 포맷 수정 (`makeMD.md`)
AI가 생성하는 마크다운 파일의 구조나 질문 내용을 변경하고 싶다면 `makeMD.md` 파일의 프롬프트를 수정하세요. Obsidian(옵시디언) 등의 도구에 맞게 템플릿을 변경할 수 있습니다.

### 상세 로직 수정 (`execution/`)
- `fetch_rss.py`: RSS 뉴스 수집 및 필터링 로직 담당.
- `process_content.py`: Gemini를 통한 요약 및 파일 생성 로직 담당.
- `git_sync.py`: GitHub 저장소 복사 및 커밋/푸시 로직 담당.

---

## 🔗 GitHub 저장소 연동 필독

이 프로젝트는 현재 작업 중인 폴더가 아닌, **다른 GitHub 저장소(예: 지식 관리 저장소)**에 파일을 자동으로 반영하도록 설계되어 있습니다.

1. **저장소 준비**: 연동할 target 저장소가 로컬 PC의 특정 경로에 이미 `git clone` 되어 있어야 합니다.
2. **권한 설정**: 해당 저장소에 대해 `git push` 권한이 있어야 하며, SSH 키 등록이나 자격 증명 헬퍼를 통해 터미널에서 비밀번호 입력 없이 푸시가 가능한 상태여야 합니다.
3. **경로 지정**: `.env` 파일의 `AMUZ_MEMO_PATH`에 해당 저장소의 **절대 경로**를 정확히 입력해야 합니다.

---

## 📁 프로젝트 구조
- `main.py`: 통합 실행 엔트리 포인트
- `run.sh`: 실행 편의를 위한 쉘 스크립트
- `execution/`: 단계별 실행 스크립트 모음
- `news/`: 생성된 뉴스 파일들이 임시 저장되는 곳 (동기화 시 복사됨)
- `.env`: API 키 및 환경 설정 정보 (보안 주의)
