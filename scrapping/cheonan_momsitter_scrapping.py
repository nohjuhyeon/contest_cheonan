from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 권한 요청을 미리 차단
prefs = {
    "profile.default_content_setting_values.notifications": 2  # 1: 허용, 2: 차단
}

# Chrome 옵션 설정
chrome_options = Options()
# 내 계정 사용 
chrome_options.add_argument("user-data-dir=/Users/ojisu/Library/Application Support/Google/Chrome/Profile 3")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--headless")  # 백그라운드 실행 (필요시)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--v=1")

chrome_options.add_experimental_option("prefs", prefs)
# ChromeDriver 서비스 객체 생성
service = Service('/usr/local/bin/chromedriver')

# ChromeDriver로 브라우저 인스턴스 생성
browser = webdriver.Chrome(service=service, options=chrome_options)

# 브라우저를 사용하여 작업 수행
browser.get("https://www.mom-sitter.com/search/sitter")

def dbconnect(collection_name):
    # MongoDB 클라이언트 설정
    mongoClient = MongoClient("mongodb://localhost:27017")
    database = mongoClient["data_cheonan"]
    collection = database[collection_name]
    return collection

# JavaScript를 사용하여 요소가 생성될 때까지 대기
def wait_for_element(selector):
    WebDriverWait(browser, 20).until(
        lambda driver: driver.execute_script("return document.querySelector(arguments[0]) != null;", selector),
        selector
    )

# 스크롤을 내리는 함수
def scroll_down():
    scrollable_div = browser.find_element(by=By.CSS_SELECTOR, value=".listPanel")

    previous_scroll_height = browser.execute_script("return arguments[0].scrollHeight", scrollable_div)
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)

    time.sleep(2)  # 스크롤 후 로딩 시간 대기

    new_scroll_height = browser.execute_script("return arguments[0].scrollHeight", scrollable_div)

    print(f"Previous scroll height: {previous_scroll_height}, New scroll height: {new_scroll_height}")

    if previous_scroll_height == new_scroll_height:
        print("더 이상 스크롤할 수 없습니다.")
    else:
        print("새로운 콘텐츠가 로드되었습니다.")





def scrape_sitter() :
    # 시터 정보 가져오기
    sitters = browser.find_elements(by=By.CSS_SELECTOR, value="div.sc-hTBuwn.kXKcCc")

    # 시터 수 만큼 반복
    for sitter in sitters:
        # 시터 이름(중복확인용)
        name = sitter.find_element(by=By.CSS_SELECTOR, value="div.basicProfileContainer > div.profileInfo > div:nth-child(1) > span:nth-child(1)").text
        # 시터 나이
        age = sitter.find_element(by=By.CSS_SELECTOR, value="div.basicProfileContainer > div.profileInfo > div:nth-child(1) > span:nth-child(2)").text
        # 희망 시급
        wage = sitter.find_element(by=By.CSS_SELECTOR, value="div.basicProfileContainer > div.profileInfo > div:nth-child(2) > p").text
        # 인증내역
        try : 
            certinfo = sitter.find_element(by=By.CSS_SELECTOR, value="div.certInfoWrap > div").text
        except :
            certinfo=''
        collection = dbconnect("momsitter_by_type")
        collection.insert_one({"name": name, "age": age, "wage":wage, "certinfo": certinfo})

while True :
    scrape_sitter()
    scroll_down()
# 브라우저 종료
browser.quit()
