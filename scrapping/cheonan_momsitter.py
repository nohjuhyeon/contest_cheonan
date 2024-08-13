import requests
import json

# API URL
url = "https://api.mom-sitter.com/api/v1/sitters/search"

# 요청 헤더 설정
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Referer": "https://www.mom-sitter.com/"
}

# 요청 데이터 설정
data = {
    "locations": "충청남도",

}

# API 요청 보내기
response = requests.post(url, headers=headers, data=json.dumps(data))

# 응답 데이터 확인
if response.status_code == 200:
    result = response.json()  # JSON 형식으로 변환
    print(result)  # 데이터 출력
else:
    print("Error Code:", response.status_code)


import json
from pymongo import MongoClient

# MongoDB에 연결
client = MongoClient('mongodb://localhost:27017/')  # 로컬 MongoDB에 연결
db = client['data_cheonan']  # 사용할 데이터베이스 이름
collection = db['momsitter']  # 사용할 컬렉션 이름

# JSON 파일 읽기
with open('data.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)  # JSON 파일을 읽어들임

# JSON 데이터를 MongoDB에 저장
if isinstance(json_data, list):
    # JSON 데이터가 리스트인 경우
    result = collection.insert_many(json_data)
else:
    # JSON 데이터가 단일 객체인 경우
    result = collection.insert_one(json_data)

print(f'Data inserted with record ids: {result.inserted_ids}')  # 삽입된 레코드 ID 출력
