import json
import os
import hashlib
import requests
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from git_sync import sync_to_github

# .env 파일 로드
load_dotenv()

# Gemini API 설정
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
else:
    model = None

def generate_hash(url):
    """URL을 기반으로 8자리 해시 생성"""
    return hashlib.sha256(url.encode()).hexdigest()[:8]

def clean_md_content(content):
    """LLM 응답에서 마크다운 코드 블록 래퍼 등을 제거"""
    content = content.strip()
    if content.startswith("```"):
        # ```markdown 또는 ``` 으로 시작하는 블록 제거
        lines = content.split('\n')
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        content = '\n'.join(lines).strip()
    return content

def slugify(text):
    """파일명으로 사용 가능한 간단한 키워드 추출 (간소화된 구현)"""
    import re
    # 한글, 영문, 숫자만 남기고 공백을 하이픈으로 변경
    text = re.sub(r'[^a-zA-Z0-9가-힣\s]', '', text)
    text = text.strip().replace(' ', '-')
    return text[:20]  # 최대 20자 제한

def process_news():
    # 1. 수집된 뉴스 로드
    latest_news_path = os.path.join(os.path.dirname(__file__), '..', '.tmp', 'latest_news.json')
    if not os.path.exists(latest_news_path):
        print("수집된 뉴스가 없습니다. fetch_rss.py를 먼저 실행하세요.")
        return

    with open(latest_news_path, 'r', encoding='utf-8') as f:
        news_items = json.load(f)

    # 2. 프롬프트 지침 로드 (makeMD.md)
    makemd_path = os.path.join(os.path.dirname(__file__), '..', 'makeMD.md')
    with open(makemd_path, 'r', encoding='utf-8') as f:
        prompt_instruction = f.read()

    # AMUZ_MEMO_PATH 경로 가져오기
    amuz_memo_path = os.getenv("AMUZ_MEMO_PATH")
    if not amuz_memo_path:
        print("에러: .env 파일에 AMUZ_MEMO_PATH가 설정되지 않았습니다.")
        return

    # 저장될 최종 디렉토리 (기존 git_sync.py의 dest_dir와 일치시킴)
    news_dir = os.path.join(amuz_memo_path, '000.Data', 'AI News')
    os.makedirs(news_dir, exist_ok=True)

    for item in news_items:
        url = item['link']
        title = item['title']
        source = item['source']
        summary = item['summary']
        pub_date = item['published'].split(' ')[0] # YYYY-MM-DD
        
        file_hash = generate_hash(url)
        keyword = slugify(title)
        filename = f"{pub_date}-{keyword}-{file_hash}.md"
        file_path = os.path.join(news_dir, filename)

        # OVERWRITE 환경변수가 'true'이면 기존 파일이 있어도 다시 처리
        overwrite = os.getenv("OVERWRITE", "false").lower() == "true"
        if os.path.exists(file_path) and not overwrite:
            print(f"이미 존재하는 파일(건너뜀): {filename}")
            continue

        print(f"처리 중: {title}")

        if model:
            import time
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # 응답 형식을 더 엄격하게 제한하기 위해 시스템 프롬프트 형식으로 결합
                    full_prompt = f"""{prompt_instruction}

위 지침을 반드시 준수하여 마크다운 노트를 작성해. 
**중요: 출력은 마크다운 코드 블록(```markdown ... ```)으로 감싸지 말고, 순수 마크다운 텍스트만 출력해.**

[분석할 뉴스 데이터]
소스: {source}
제목: {title}
링크: {url}
내용 요약: {summary}
현재 날짜: {pub_date}
"""
                    response = model.generate_content(full_prompt)
                    md_content = clean_md_content(response.text)
                    
                    # 파일 저장
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(md_content)
                    print(f" - 저장 완료: {filename}")
                    
                    # 429 방지를 위해 요청 간 지연
                    time.sleep(5)
                    break
                except Exception as e:
                    if "429" in str(e) and attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 10
                        print(f" - API 할당량 초과 (429). {wait_time}초 후 재시도... ({attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                    else:
                        print(f" - LLM 처리 에러: {e}")
                        break
        else:
            print(" - GOOGLE_API_KEY가 설정되지 않아 처리를 건너뜁니다.")

    # 3. 모든 뉴스 처리 완료 후 GitHub 동기화 실행
    print("\n--- GitHub 동기화 시작 ---")
    sync_to_github()

if __name__ == "__main__":
    process_news()
