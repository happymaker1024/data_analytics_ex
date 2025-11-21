from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from pprint import pprint

# 1. 웹드라이버 옵션 설정 및 객체 생성
options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR')
options.add_experimental_option("excludeSwitches", ["enable-logging"])

chrome = webdriver.Chrome(options=options)

wait = WebDriverWait(chrome, 10)  # 명시적 대기 객체

url = "https://map.kakao.com/"
chrome.get(url)



# 2. 검색어 입력 및 검색 실행
search_area = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search.keyword.query"]')))
search_area.send_keys("스타벅스")

submit_btn = chrome.find_element(By.XPATH, '//*[@id="search.keyword.submit"]')
submit_btn.send_keys(Keys.ENTER)

# 검색 결과 리스트 로딩 대기
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.placelist > li.PlaceItem')))
cafe_lists = chrome.find_elements(By.CSS_SELECTOR, 'ul.placelist > li.PlaceItem')
print(len(cafe_lists))

place_reviews = {}

for i, cafe in enumerate(cafe_lists):
    try:
        place_name = cafe.find_element(By.CSS_SELECTOR, '.head_item .link_name').text
        print(place_name)

        # 상세보기 클릭 (새 탭 열림)
        x_path = f'//*[@id="info.search.place.list"]/li[{i+1}]/div[5]/div[4]/a[1]'
        detail_btn = wait.until(EC.element_to_be_clickable((By.XPATH, x_path)))
        detail_btn.send_keys(Keys.ENTER)

        # 새 탭이 열릴 때까지 기다린 후 전환
        wait.until(lambda d: len(d.window_handles) > 1)
        chrome.switch_to.window(chrome.window_handles[-1])

        # 리뷰 목록이 로딩될 때까지 대기
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.list_review > li")))

        # "더보기" 버튼 클릭 (있을 경우만)
        review_items = chrome.find_elements(By.CSS_SELECTOR, ".list_review > li")
        for review in review_items:
            try:
                more_btn = review.find_element(By.CSS_SELECTOR, "span.btn_more")
                if more_btn.is_displayed() and more_btn.is_enabled():
                    more_btn.click()
                    time.sleep(0.2)
            except:
                continue

        # 리뷰 텍스트 추출
        review_elements = chrome.find_elements(By.CSS_SELECTOR, "ul.list_review li .wrap_review p.desc_review")
        one_place_reviews = []
        for review_elem in review_elements:
            try:
                one_place_reviews.append(review_elem.text)
            except:
                continue

        place_reviews[place_name] = one_place_reviews

        chrome.close()
        chrome.switch_to.window(chrome.window_handles[0])  # 첫 탭으로 복귀

    except Exception as e:
        print(f"[오류] {e}")
        continue

# 리뷰 데이터 출력 및 저장
pprint(place_reviews)

try:
    with open('./star_reviews_data.json', 'w', encoding='utf-8') as f:
        json.dump(place_reviews, f, ensure_ascii=False, indent=4)
except Exception as e:
    print(f"예외 발생 : {e}")

chrome.quit()
