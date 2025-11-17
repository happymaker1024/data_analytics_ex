from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time

# 서비스 객체생성
service = Service(ChromeDriverManager().install())
chrome = webdriver.Chrome(service=service)
chrome.get("http://naver.com")  # page를 가져옴

# 5초를 기다림
# time.sleep(10) # 3sec
# chrome.implicitly_wait(3)    # 크롬드라이브와 통신하는 지점에서 delay

WebDriverWait(chrome, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name=query]"))
    )

chrome.close()