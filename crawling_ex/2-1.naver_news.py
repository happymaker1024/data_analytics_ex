# 1. 라이브러리 로딩
from bs4 import BeautifulSoup as BS
import urllib.request as req
import datetime
import os
import csv
from datetime import datetime

# 2. html 문서 가져오기
naver_url = "https://news.naver.com/section/100"

html = req.urlopen(naver_url)

#3. HTML 파싱하기
soup = BS(html, "html.parser")
# print(soup)

# 4. 뉴스 목록 (li태그) 추출하기 <- list
# 반복되는 패턴을 찾아서 셀렉터로 지정
#  ul.sa_list > li
lis = soup.select("ul.sa_list > li")
# print(len(lis))
news_lists = []
for li in lis:
    title = li.select_one("strong.sa_text_strong").get_text()
    press = li.select_one("div.sa_text_press").get_text()
    img_url = li.select_one("img")
    # print(img_url)
    if img_url:
        img_url = img_url.get("src") or img_url.get("data-src")
        img_url = img_url.split("?")[0]
    else:
        img_url = "이미지 없음"
    # 추출한 목록 프린트
    # print(f"{title}, {press}, {img_url}")

    # 하나의 뉴스 정보를 전체목록 시스트에 추가
    news_lists.append([title, press, img_url])
print(news_lists)

# 6. 리스트 -> 파일에 저장
# 현재 날짜/시간 가져오기
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d-%H")   # → 2025-11-17-13 형태

# 폴더 / 파일명 설정
folder = "naver_news"
filename = f"{timestamp}.csv"
filepath = os.path.join(folder, filename)

# 폴더 자동 생성
os.makedirs(folder, exist_ok=True)

# CSV 저장 (2차원 리스트 여야함.)
with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["헤드라인","신문사","이미지url"])
    writer.writerows(news_lists)

print("CSV 저장 완료:", filepath)

