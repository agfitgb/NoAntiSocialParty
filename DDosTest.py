import requests
import time

url = "https://ce3f08de8beb.ngrok-free.app/"  # 접속할 URL
delay = 1  # 요청 간격(초)

while True:
    try:
        response = requests.get(url)
        print(f"[{response.status_code}] 요청 성공")
    except Exception as e:
        print(f"요청 실패: {e}")
    time.sleep(delay)
