import requests as req
from bs4 import BeautifulSoup as BS
import datetime
import os

# naver_url = "https://news.naver.com/"
news_url = "https://news.naver.com/section/100"

html = req.get(news_url).text
soup = BS(html, 'html.parser')
# print(soup)
elem_list = soup.select('ul.sa_list li.sa_item')
# print(elem_list)

# news headline 만 추출
searchword_list = []
for elem in elem_list:
    # print(elem)
    head_line = elem.select_one('.sa_text_strong').get_text().strip()
    newspaper = elem.select_one('.sa_text_press').get_text().strip()
    # 이미지 src 추출 (.sa_thumb_inner 아래의 img 태그)
    img_url = elem.select_one('.sa_thumb_inner img')
    # lazy-loading일 경우 data-src 등에 있을 수 있으므로 우선순위로 가져옴
    if img_url:
        img_url = img_url.get('src') or img_url.get('data-src') or ''
        img_url = img_url.split('?')[0]  # URL 파라미터 제거
    else:
        img_url = 'img url 없음'
    # 터미널 출력
    print(f"{head_line} - {newspaper}\nImage URL: {img_url}")
    # list에 추가 : 뉴스 한 개에 대한 수집 정보
    searchword_list.append([head_line, newspaper, img_url])

# 저장할 파일 이름 구하기
base_path = 'naver_news/'
os.makedirs(base_path, exist_ok=True)

# 파일이름 정의, 날짜로 정의 (yyyy-mm-dd-h)
t = datetime.datetime.today()
fname = base_path + t.strftime('%Y-%m-%d-%H') + '.csv'
with open(fname, 'w', encoding="utf-8") as f:
    for news in searchword_list:
        f.write(','.join(news) + '\n')
