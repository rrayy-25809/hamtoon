import requests
import json

def fetch_webtoon_data():
    base_url = "https://webtoon-crawler.nomadcoders.workers.dev"
    endpoint = "today"
    url = f"{base_url}/{endpoint}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        
        print("응답 상태 코드:", response.status_code)
        print("응답 내용:", response.text[:500])  # 응답 내용 일부 출력

        data = response.json()  # JSON 데이터 파싱
        
        # 웹툰 목록 출력
        for webtoon in data:
            title = webtoon.get("title", "제목 없음")
            author = webtoon.get("author", "작가 미상")
            print(f"제목: {title}, 작가: {author}")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 에러 발생: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"요청 에러 발생: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON 디코딩 에러 발생: {json_err}")

# 함수 실행
if __name__ == "__main__":
    fetch_webtoon_data()
