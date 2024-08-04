## dbmongo의 collection 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://localhost:27017/")
# database 연결
database = mongoClient["healthcare_project"]
# collection 작업
collection = database['PMC_FHP_data']
# insert 작업 진행
# 크롤링 동작
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
# Chrome 브라우저 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

# WebDriver 서비스 생성
service = ChromeService(executable_path=ChromeDriverManager().install())

browser = webdriver.Chrome(service=service, options=chrome_options)

# 크롤링할 웹 페이지 URL
url = "https://cafe.naver.com/imsanbu"
# 웹 페이지 열기
html_source = browser.get(url)
pass

login_path = browser.find_element(by=By.CSS_SELECTOR,value='#gnb_login_button > span.gnb_txt')
login_path.click()
pass
time.sleep(3)
id_box = browser.find_element(by=By.CSS_SELECTOR,value='#id')
id_box.send_keys('')
pwd_box = browser.find_element(by=By.CSS_SELECTOR,value='#pw')
pwd_box.send_keys('')
pass
login_btn = browser.find_element(by=By.CSS_SELECTOR,value='#log\.login')
login_btn.click()
pass