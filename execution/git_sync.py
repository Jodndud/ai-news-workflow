import os
import shutil
import subprocess
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def sync_to_github():
    """
    news/ 디렉토리의 파일을 amuz-memo 저장소로 복사하고 Git 커밋/푸시를 수행합니다.
    """
    basic_path = os.getenv("BASIC_PATH")
    if not basic_path:
        print("에러: .env 파일에 BASIC_PATH가 설정되지 않았습니다.")
        return

    # 2. Git 동기화 대상 디렉토리 설정
    news_subdir = os.getenv("NEWS_SUBDIR")
    if not news_subdir:
        print("에러: .env 파일에 NEWS_SUBDIR가 설정되지 않았습니다.")
        return
    dest_dir = os.path.join(basic_path, news_subdir)
    if not os.path.exists(dest_dir):
        print(f"경고: 동기화할 디렉토리가 존재하지 않습니다: {dest_dir}")
        return

    print(f"동기화 경로 확인됨: {dest_dir}")

    # 4. Git 작업 수행
    try:
        print(f"Git 작업 시작 (저장소: {basic_path})")
        
        # git add
        subprocess.run(['git', 'add', '.'], cwd=basic_path, check=True)
        
        # git status 확인하여 변경사항 있는지 체크
        status_proc = subprocess.run(['git', 'status', '--porcelain'], cwd=basic_path, capture_output=True, text=True)
        if not status_proc.stdout.strip():
            print("변경사항이 없어 커밋을 건너뜁니다.")
            return

        # git commit
        commit_message = f"Auto-sync AI News: {os.path.basename(filename) if 'filename' in locals() else 'New updates'}"
        subprocess.run(['git', 'commit', '-m', commit_message], cwd=basic_path, check=True)
        
        # git push
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=basic_path, check=True)
        
        print("GitHub 푸시 완료!")
        
    except subprocess.CalledProcessError as e:
        print(f"Git 작업 중 에러 발생: {e}")
    except Exception as e:
        print(f"알 수 없는 에러 발생: {e}")

if __name__ == "__main__":
    sync_to_github()
