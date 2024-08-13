import requests
import json
from pymongo import MongoClient

def dbconnect(collection_name):
    # MongoDB에 연결
    client = MongoClient('mongodb://localhost:27017/')  # 로컬 MongoDB에 연결
    db = client['data_cheonan']  # 사용할 데이터베이스 이름
    collection = db[collection_name]  # 사용할 컬렉션 이름
    return collection

activity_dict = [{6: "실내놀이"},
                 {13: "등하원돕기"},
                 {10: "책읽기"},
                 {7: "야외활동"},
                 {14: "한글놀이"},
                 {19: "영어놀이"},
                 {51: "학습지도"},
                 {8: "체육놀이"},
                 {5: "간단청소"},
                 {3: "밥챙겨주기"},
                 {4: "간단설거지"},
                 {2: "장기입주"},
                 {1: "단기입주"}]

for activity in activity_dict:
    page = 1

    while True:
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
        body = {
            "activityIds": [list(activity.keys())[0]],
            "location": "충청남도 천안시 동남구 전체",
            "locationDescription": "충청남도 천안시 동남구 전체",
            "locationTerm": {"main": "충청남도", "sub": "천안시 동남구", "detail": "전체"},
            "detail": "전체",
            "main": "충청남도",
            "sub": "천안시 동남구",
            "page": page
        }

        # API 요청 보내기
        response = requests.post(url, headers=headers, json=body)
        contents = json.loads(response.content)

        # MongoDB 연결
        collection = dbconnect("momsitter_east")
        
        # sitters 리스트가 빈 경우 while 루프 종료
        try :
            if not contents['sitters']:
                break

            # sitters 리스트에서 각 sitter를 검사
            for sitter in contents['sitters']:
                # 특정 필드가 빈 리스트인지 확인
                if 'some_field' in sitter and not sitter['some_field']:
                    # 빈 리스트일 경우, while 루프 종료
                    break
                sitter['activity'] = list(activity.values())[0]
                collection.insert_one(sitter)
            else:
                # 모든 sitter가 처리되었고 빈 리스트가 없었을 경우 페이지 증가
                page += 1
                continue

            # 빈 리스트가 발견된 경우 while 루프 종료
            break
        except :
            break