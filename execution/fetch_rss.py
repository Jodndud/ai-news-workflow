import json
import os
import feedparser
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def fetch_news():
    # 프로젝트 루트 경로 가져오기
    project_root = os.getenv("PROJECT_ROOT", os.path.join(os.path.dirname(__file__), '..'))
    
    # RSS 리스트 읽기
    rss_list_path = os.path.join(project_root, 'RSSList.json')
    with open(rss_list_path, 'r', encoding='utf-8') as f:
        sources = json.load(f)

    all_news = []
    now = datetime.now()
    yesterday = now - timedelta(hours=24)

    for source in sources:
        name = source['source_name']
        url = source['url']
        print(f"[{name}] 수집 중: {url}")

        try:
            feed = feedparser.parse(url)
            count = 0
            for entry in feed.entries:
                if count >= 5:
                    break

                # 게시일 파싱
                published_struct = entry.get('published_parsed') or entry.get('updated_parsed')
                if published_struct:
                    published_dt = datetime.fromtimestamp(time.mktime(published_struct))
                    
                    # 24시간 이내 필터링
                    if published_dt > yesterday:
                        all_news.append({
                            'source': name,
                            'title': entry.title,
                            'link': entry.link,
                            'published': published_dt.strftime('%Y-%m-%d %H:%M:%S'),
                            'summary': entry.get('summary', '') or entry.get('description', '')
                        })
                        count += 1
            
            print(f" - {count}개의 새로운 게시물 발견")
        except Exception as e:
            print(f" - 에러 발생: {e}")

    # 결과 저장 (임시 파일)
    tmp_dir = os.path.join(project_root, '.tmp')
    os.makedirs(tmp_dir, exist_ok=True)
    
    output_path = os.path.join(tmp_dir, 'latest_news.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    print(f"\n최종 {len(all_news)}개의 뉴스가 {output_path}에 저장되었습니다.")

if __name__ == "__main__":
    fetch_news()
