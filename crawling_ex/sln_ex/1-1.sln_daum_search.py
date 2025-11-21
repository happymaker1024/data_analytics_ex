# 1. 라이브러리 로딩
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time  

# 2. 웹 드라이버 객체생성

# 1) 옵션 정의
options = webdriver.ChromeOptions()             # 옵션 설정 객체 생성
options.add_argument("window-size=1000,1000")   # 브라우저 크기 설정(가로 x 세로)
options.add_argument("no-sandbox")              # 샌드박스 사용 안하겠다. 텝별로 분리하겠다. 거리를 두겠다
# options.add_argument("headless")              # 크롬 창을 안뜨게함.
options.add_experimental_option("excludeSwitches", ["enable-logging"]) 

chrome = webdriver.Chrome(options=options) 

# 3. 웹드라이버를 통해 url의 페이지 가져오기
chrome.get("http://daum.net")

# 4. 페이지 로딩까지 기다림
wait = WebDriverWait(chrome, 2) 
def find(wait, css_selector):
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

# 5. 원하는 요소(태그)가 로딩할 때까지 기다림
search = find(wait, "input[name=q]")

chrome.find_element(By.ID, "q").clear()
time.sleep(3) # 간단한 delay, 파이썬 라이브러리

# 6. 검색 키워드 입력
search.send_keys("사과")
# chrome.find_element_by_id("daumBtnSearch").click()
search.send_keys(Keys.ENTER)
#elem.click()
time.sleep(3) # 간단한 delay, 파이썬 라이브러리

# 7. 원한 요소의 텍스트나 이미지를 추출
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

# 8. 웹드라이브 종료
chrome.close()
#chrome.quit() # tab 모두 종료