# webdriver_manager 를 활용하여 크롬 드라이버 연결하기
## [usage : ]
## pip install webdriver-manager 설치 하기
## from webdriver_manager.chrome import ChromeDriverManager
## chrome = webdriver.Chrome(ChromeDriverManager().install(), options=options)
###############################################################################
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time  

options = webdriver.ChromeOptions()             # 옵션 설정 객체 생성
options.add_argument("window-size=1000,1000")   # 브라우저 크기 설정(가로 x 세로)
options.add_argument("no-sandbox")              # 샌드박스 사용 안하겠다. 텝별로 분리하겠다. 거리를 두겠다
# options.add_argument("headless")              # 크롬 창을 안뜨게함.
options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 
# ChromeDriver 경로를 지정하는 Service 객체 생성
# service = Service(ChromeDriverManager().install())
# chrome = webdriver.Chrome(service=service, options=options) 
chrome = webdriver.Chrome(options=options) 

chrome.get("http://daum.net")

wait = WebDriverWait(chrome, 10) 
def find(wait, css_selector):
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

search = find(wait, "input[name=q]")

chrome.find_element(By.ID, "q").clear()
time.sleep(3) # 간단한 delay, 파이썬 라이브러리
search.send_keys("사과")
# chrome.find_element_by_id("daumBtnSearch").click()
search.send_keys(Keys.ENTER)
#elem.click()
time.sleep(3) # 간단한 delay, 파이썬 라이브러리

# items = chrome.find_elements_by_class_selector("thumb_img")
items = chrome.find_elements(By.CSS_SELECTOR, ".list_shopping .wrap_thumb img")
time.sleep(3) # 간단한 delay, 파이썬 라이브러리
#print(items)
for item in items:
    print(item.get_attribute("src"))

chrome.back()
time.sleep(2)
chrome.forward()
time.sleep(2)
chrome.close()
#chrome.quit() # tab 모두 종료


#### 다양한 엘리먼트 얻는 방법
# 참고 : https://wikidocs.net/177133