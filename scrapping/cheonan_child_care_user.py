import requests
import json
from pymongo import MongoClient

def dbconnect(collection_name):
    # MongoDB에 연결
    client = MongoClient('mongodb://localhost:27017/')  # 로컬 MongoDB에 연결
    db = client['contest_cheonan']  # 사용할 데이터베이스 이름
    collection = db[collection_name]  # 사용할 컬렉션 이름
    return collection

url = "https://apis.data.go.kr/1383000/idis/memberService/getMemberList?serviceKey=Qa6CXT4r6qEr%2BkQt%2FJx6wJr5MPx45hKNJwNTScoYryT2uGz7GozIqpjBw%2FRMk1uE8l92NU7h89m20sa%2FXHKuaQ%3D%3D&pageNo=1&type=json&numOfRows=100&crtrYmFrom=202001&crtrYmTo=202312&childCareInstNo=C0287"

        # 요청 헤더 설정
        # headers = {
        #     "Content-Type": "application/json",
        #     "Accept": "application/json",
        #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        #     "Referer": "https://www.mom-sitter.com/"
        # }

        # # 요청 데이터 설정
        # body = {
        #     "activityIds": [list(activity.keys())[0]],
        #     "location": "충청남도 천안시 동남구 전체",
        #     "locationDescription": "충청남도 천안시 서북구 전체",
        #     "locationTerm": {"main": "충청남도", "sub": "천안시 서북구", "detail": "전체"},
        #     "detail": "전체",
        #     "main": "충청남도",
        #     "sub": "천안시 서북구",
        #     "page": page
        # }

        # API 요청 보내기
response = requests.get(url)
contents = json.loads(response.content)
contents = contents['response']['body']['items']['item']
        # MongoDB 연결
collection = dbconnect("child_care_user")

for i in contents:
      dict_center = {}
      dict_center['date'] = i['crtrYm']
      dict_center['center_name'] = i['childCareInstNm']
      dict_center['total_members'] = i['whlMbrCnt']
      dict_center['web_members'] = i['webMbrCnt']
      dict_center['pending_approval_members'] = i['aprvStdbyMbrCnt']
      dict_center['regular_members'] = i['rglmbrCnt']
      dict_center['periodic_regular_members'] = i['prdclRglmbrCnt']
      dict_center['pending_regular_members'] = i['stdbyRglmbrCnt']
      dict_center['dormant_members'] = i['drmntMbrCnt']
      dict_center['new_members'] = i['newMbrCnt']
      dict_center['new_children'] = i['newChildCnt']
      collection.insert_one(dict_center)
# # sitters 리스트가 빈 경우 while 루프 종료
# try :
#     if not contents['sitters']:
#         break

#     # sitters 리스트에서 각 sitter를 검사
#     for sitter in contents['sitters']:
#         # 특정 필드가 빈 리스트인지 확인
#         if 'some_field' in sitter and not sitter['some_field']:
#             # 빈 리스트일 경우, while 루프 종료
#             break
#         sitter['activity'] = list(activity.values())[0]
#         collection.insert_one(sitter)
#     else:
#         # 모든 sitter가 처리되었고 빈 리스트가 없었을 경우 페이지 증가
#         page += 1
#         continue

#     # 빈 리스트가 발견된 경우 while 루프 종료
#     break
# except :
#     break