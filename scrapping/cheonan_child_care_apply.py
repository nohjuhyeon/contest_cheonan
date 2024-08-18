# url : https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15078106 
import requests
import json
from pymongo import MongoClient

def dbconnect(collection_name):
    # MongoDB에 연결
    client = MongoClient('mongodb://localhost:27017/')  # 로컬 MongoDB에 연결
    db = client['contest_cheonan']  # 사용할 데이터베이스 이름
    collection = db[collection_name]  # 사용할 컬렉션 이름
    return collection

url = "https://apis.data.go.kr/1383000/idis/aplyService/getAplyList?serviceKey=Qa6CXT4r6qEr%2BkQt%2FJx6wJr5MPx45hKNJwNTScoYryT2uGz7GozIqpjBw%2FRMk1uE8l92NU7h89m20sa%2FXHKuaQ%3D%3D&pageNo=1&type=json&numOfRows=200&crtrYmFrom=202001&crtrYmTo=202312&childCareInstNo=C0287"


        # API 요청 보내기
response = requests.get(url)
contents = json.loads(response.content)
contents = contents['response']['body']['items']['item']
        # MongoDB 연결
collection = dbconnect("child_care_apply")

for i in contents:
      dict_center = {}
      dict_center['date'] = i['crtrYm']
      dict_center['center_name'] = i['childCareInstNm']
      dict_center['disease_child'] = i['ilnsSrvcYn']
      dict_center['care_type'] = i['careDvsnNm']
      dict_center['service_type'] = i['srvcDvsfctnNm']
      dict_center['total_applications'] = i['whlAplyNocs']
      dict_center['linked_applications'] = i['linkAplyNocs']
      dict_center['linked_applications_type_a'] = i['linkAtypeAplyNocs']
      dict_center['linked_applications_type_b'] = i['linkBtypeAplyNocs']
      dict_center['linked_applications_type_c'] = i['linkCtypeAplyNocs']
      dict_center['linked_applications_type_d'] = i['linkDtypeAplyNocs']
      dict_center['applications'] = i['aplyNocs']
      dict_center['applications_type_a'] = i['atypeAplyNocs']
      dict_center['applications_type_b'] = i['btypeAplyNocs']
      dict_center['applications_type_c'] = i['ctypeAplyNocs']
      dict_center['applications_type_d'] = i['dtypeAplyNocs']
      collection.insert_one(dict_center)
