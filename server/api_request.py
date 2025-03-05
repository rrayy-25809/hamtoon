import requests
import json
import html

base_url = "https://webtoon-crawler.nomadcoders.workers.dev"

def fetch_today_webtoon() -> dict | None:
    url = base_url + "/today" # 엔드포인트를 today로 설정
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        
        print("응답 상태 코드:", response.status_code)

        return response.json()  # JSON 데이터 파싱
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 에러 발생: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"요청 에러 발생: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON 디코딩 에러 발생: {json_err}")

def fetch_webtoon_detail(webtoon_id) -> dict | None:
    # 웹툰 상세 정보 API 요청
    url = f"{base_url}/{webtoon_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리

        print("응답 상태 코드:", response.status_code)

        detail:dict = response.json()  # JSON 데이터 파싱
        detail["about"] = html.unescape(detail["about"])  # HTML 엔티티를 원래 문자로 변환
        detail["id"] = webtoon_id
        if detail["thumb"] == "":   # 썸네일 이미지가 없는 경우 대체 이미지 사용
            detail["thumb"] = "https://w7.pngwing.com/pngs/668/494/png-transparent-specials-unicode-character-ersetzungszeichen-code-point-rectangle-border-miscellaneous-angle-text.png"
        return detail

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 에러 발생: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"요청 에러 발생: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON 디코딩 에러 발생: {json_err}")

def fetch_webtoon_episode(webtoon_id) -> dict | None:
    # 웹툰 에피소드 목록 API 요청
    url = f"{base_url}/{webtoon_id}/episodes"

    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리

        print("응답 상태 코드:", response.status_code)
        
        detail = response.json()  # JSON 데이터 파싱

        #return detail
        print(detail[0])

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 에러 발생: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"요청 에러 발생: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"JSON 디코딩 에러 발생: {json_err}")

if __name__ == "__main__":
    print(fetch_webtoon_episode(824888))