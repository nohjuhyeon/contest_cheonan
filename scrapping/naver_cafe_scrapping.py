## dbmongo의 collection 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://localhost:27017/")
# database 연결
database = mongoClient["contest_cheonan"]
# collection 작업
collection = database['baby_care_reaction']
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
def content_scrapping(browser):
    content_list = browser.find_elements(by=By.CSS_SELECTOR,value='a.article')
    for i in range(len(content_list)):
        while True:
            try:
                content_list = browser.find_elements(by=By.CSS_SELECTOR,value='a.article')
                content_list[i].click()
                time.sleep(1)
                title = browser.find_element(by=By.CSS_SELECTOR,value='#app > div > div > div.ArticleContentBox > div.article_header > div:nth-child(1) > div > div > h3').text
                try:
                    contents = browser.find_element(by=By.CSS_SELECTOR,value='div.content.CafeViewer').text
                except:
                    contents = browser.find_element(by=By.CSS_SELECTOR,value='div.ContentRenderer').text
                date = browser.find_element(by=By.CSS_SELECTOR,value='span.date').text
                like_count = browser.find_element(by=By.CSS_SELECTOR,value='#app > div > div > div.ArticleContentBox > div.article_container > div.ReplyBox > div.box_left > div > div > a > em.u_cnt._count').text
                review_btn_list = browser.find_elements(by=By.CSS_SELECTOR,value='#app > div > div > div.ArticleContentBox > div.article_container > div.CommentBox > div.ArticlePaginate > button')
                if len(review_btn_list) == 0:
                    review_list = browser.find_elements(by=By.CSS_SELECTOR,value='div > div > div.comment_text_box > p')
                    if len(review_list) != 0:
                        for j in review_list:
                            review = j.text
                            print(title)
                            print(contents)
                            print(date)
                            print(like_count)
                            print(review)
                            collection.insert_one({"title": title,"date":date,"contents":contents,'like':like_count,'review':review})
                    else:
                        print(title)
                        print(contents)
                        print(date)
                        print(like_count)
                        collection.insert_one({"title": title,"date":date,"contents":contents,'like':like_count})
                else:
                    for i in review_btn_list:
                        i.click()
                        time.sleep(1)
                        review_list = browser.find_elements(by=By.CSS_SELECTOR,value='div > div > div.comment_text_box > p')
                        for j in range(len(review_list)):
                            review_list = browser.find_elements(by=By.CSS_SELECTOR,value='div > div > div.comment_text_box > p')
                            review = review_list[j].text
                            print(title)
                            print(contents)
                            print(date)
                            print(like_count)
                            print(review)
                            collection.insert_one({"title": title,"date":date,"contents":contents,'like':like_count,'review':review})
                    pass
                browser.back()
                time.sleep(1)
                browser.switch_to.frame("cafe_main")
                break
            except:
                browser.back()
                time.sleep(1)
                browser.switch_to.frame("cafe_main")
                pass

login_path = browser.find_element(by=By.CSS_SELECTOR,value='#gnb_login_button > span.gnb_txt')
login_path.click()
pass
time.sleep(3)
id_box = browser.find_element(by=By.CSS_SELECTOR,value='#id')
# id_box.send_keys('njh0205')
id_box.send_keys('whdb5893')
pwd_box = browser.find_element(by=By.CSS_SELECTOR,value='#pw')
# pwd_box.send_keys('wngus2720')
pwd_box.send_keys('njh0156!!')
pass
ip_save = browser.find_element(by=By.CSS_SELECTOR,value='#login_keep_wrap > div.ip_check > span')
ip_save.click()
time.sleep(1)
login_btn = browser.find_element(by=By.CSS_SELECTOR,value='#log\.login')
login_btn.click()
pass
search_box = browser.find_element(by=By.CSS_SELECTOR,value='#topLayerQueryInput')
search_box.send_keys('"아이돌보미"')
search_btn = browser.find_element(by=By.CSS_SELECTOR,value='#info-search > form > button')
search_btn.click()
pass
time.sleep(1)
browser.switch_to.frame("cafe_main")
content_size = browser.find_element(by=By.CSS_SELECTOR,value='#listSizeSelectDiv > a')
content_size.click()
time.sleep(1)
content_50 = browser.find_element(by=By.CSS_SELECTOR,value='#listSizeSelectDiv > ul > li:nth-child(7) > a')
content_50.click()
time.sleep(1)
search_box = browser.find_element(by=By.CSS_SELECTOR,value='#queryTop')
search_box.clear()
search_box.send_keys('"아이돌보미"')
search_btn = browser.find_element(by=By.CSS_SELECTOR,value='#main-area > div.search_result > div:nth-child(1) > form > div.input_search_area > button')
search_btn.click()
time.sleep(1)
page_btn_list = browser.find_elements(by=By.CSS_SELECTOR,value='#main-area > div.prev-next > a')

content_scrapping(browser)
while True:
    page_btn_list = browser.find_elements(by=By.CSS_SELECTOR,value='#main-area > div.prev-next > a')
    for k in range(1,len(page_btn_list)):
        page_btn_list = browser.find_elements(by=By.CSS_SELECTOR,value='#main-area > div.prev-next > a')
        page_btn_list[k].click()
        content_scrapping(browser)
    next_btn = browser.find_elements(by=By.CSS_SELECTOR,value='#main-area > div.prev-next > a.pgR > span')
    if len(next_btn) == 0:
        break

for k in range(1,len(page_btn_list)):
    page_btn_list = browser.find_elements(by=By.CSS_SELECTOR,value='#main-area > div.prev-next > a')
    page_btn_list[k].click()
    content_scrapping(browser)
pass