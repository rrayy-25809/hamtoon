import requests
import json

base_url = "https://webtoon-crawler.nomadcoders.workers.dev"

def fetch_today_webtoon():
    url = base_url + "today" # 엔드포인트를 today로 설정
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        
        print("응답 상태 코드:", response.status_code)
        print("응답 내용:", response.text[:500])  # 응답 내용 일부 출력

        return response.json()  # JSON 데이터 파싱
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 에러 발생: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"요청 에러 발생: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON 디코딩 에러 발생: {json_err}")
\
def fetch_webtoon_detail(webtoon_id):
    # 웹툰 상세 정보 API 요청
    url = f"{base_url}/{webtoon_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리

        print("응답 상태 코드:", response.status_code)
        print("응답 내용:", response.text[:500])  # 응답 내용 일부 출력

        return response.json()  # JSON 데이터 파싱
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 에러 발생: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"요청 에러 발생: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON 디코딩 에러 발생: {json_err}")