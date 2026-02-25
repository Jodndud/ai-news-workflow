import sys
import os

# execution 디렉토리를 path에 추가하여 모듈 참조 가능하게 함
sys.path.append(os.path.join(os.path.dirname(__file__), 'execution'))

from fetch_rss import fetch_news
from process_content import process_news

def main():
    print("=== AI 뉴스 워크플로우 통합 실행 시작 ===\n")
    
    # 1단계: 뉴스 수집 및 필터링
    print("[1단계] 뉴스 수집 및 필터링 시작...")
    try:
        fetch_news()
        print("[1단계] 완료\n")
    except Exception as e:
        print(f"[1단계] 오류 발생: {e}")
        return

    # 2단계: 콘텐츠 요약 및 포맷팅 (및 GitHub 동기화)
    print("[2단계] 콘텐츠 요약 및 포맷팅 시작...")
    try:
        process_news()
        print("[2단계] 완료\n")
    except Exception as e:
        print(f"[2단계] 오류 발생: {e}")
        return

    print("=== 모든 워크플로우 단계가 성공적으로 완료되었습니다. ===")

if __name__ == "__main__":
    main()
