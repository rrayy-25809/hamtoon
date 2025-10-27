import subprocess
import sys

# Npm 패키지 설치
try:
    process = subprocess.run("npm install", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')  # Vite 빌드 명령어 실행
    
    # 실시간 로그 출력
    for line in process.stdout:
        print(line, end="")
    for line in process.stderr:
        print(line, end="")

    if process.returncode != 0:
        print("❌ 빌드 실패!")
        sys.exit(1)  # 빌드 실패 시 프로그램 종료
except Exception as e:
    print(f"🚨 오류 발생: {e}")
    sys.exit(1)

print("✅ npm 패키지 설치 완료!")

# python 패키지 설치
try:
    process = subprocess.run("pip install -r requirements.txt", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')  # Vite 빌드 명령어 실행
    
    # 실시간 로그 출력
    for line in process.stdout:
        print(line, end="")
    for line in process.stderr:
        print(line, end="")

    if process.returncode != 0:
        print("❌ 빌드 실패!")
        sys.exit(1)  # 빌드 실패 시 프로그램 종료
except Exception as e:
    print(f"🚨 오류 발생: {e}")
    sys.exit(1)

print("✅ python 패키지 설치 완료!")