## 🗞️ AI News Workflow

매일아침 출근해서 AI기사를 보면서 마음을 정리를 해야지..
- *RSS 피드를 통해 최신 뉴스를 수집하고, `Google Gemini`를 통해 요약해서 마크다운 문서로 만들어주는 자동화 도구입니다.*
- *옵시디언 환경에 맞는 md 파일로 저장됩니다.*
- *이 워크플루우는 `Google Antigravity`로 제작했습니다.*

### ✨ 기능

- **24시간 내 AI 소식**: 설정해둔 RSS 피드에서 최신 기술 뉴스를 자동으로 긁어옵니다.
- **옵시디언용 요약 md파일 생성**: Gemini가 뉴스를 분석해 핵심 포인트와 인사이트를 담은 마크다운 노트를 작성합니다.
- **뉴스저장 후 깃헙에 저장까지**: (선택 사항) 로컬의 다른 저장소나 GitHub 레포지토리로 자동 동기화하여 지식 베이스를 풍성하게 채워줍니다.

### 🛠️ 설정법

#### 1. 라이브러리 설치
```bash
pip install feedparser python-dotenv google-generativeai
```

#### 2. 환경 설정 (`.env`)
`.env.example` 파일을 복사해서 내용을 채워주세요

```env
# Google Gemini API 키
GOOGLE_API_KEY=여러분의_API_키

# 파일이 저장될 로컬 경로 (예: 지식 관리 폴더)
BASIC_PATH=/Users/username/MyMemo

# 상세 저장 폴더 이름 (예: 001.Daily/News)
NEWS_SUBDIR=001.Daily/AI_News
```

#### 3. 소스 추가 (`RSSList.json`)
추가로 보고 싶은 뉴스 사이트의 RSS 주소를 `RSSList.json`에 추가하기

### 🚀 실행
```bash
./run.sh
```
or
```bash
python3 main.py
```

오늘도 AI 뉴스 워크플로우와 함께 생산성 넘치는 하루 되세요! 🚀
