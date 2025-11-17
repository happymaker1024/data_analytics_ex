from bs4 import BeautifulSoup as BS
import urllib.request as req
import datetime
import os

# HTML 가져오기
url = "https://finance.naver.com/marketindex/exchangeList.naver"
html = req.urlopen(url)

# HTML 파싱하기
soup = BS(html, "html.parser")
# print(soup)
# print(soup.prettify())

# tobdy tr td-1, td-2
# print(soup.select("tbody > tr")[0].select_one("td").get_text().strip())

trs = soup.select("tbody > tr")
# 전체 저장 리스트
exchange_list = []
for tr in trs:
    # 하나의 통화 list로 저장
    title = tr.select_one("td.tit").get_text().strip()
    sale = tr.select_one("td.sale").get_text().strip()
    exchange_list.append([title, sale])
    # print(f"{title} - {sale}")
    # print("-"*30)
    # list에 저장
print(exchange_list)
# # 파일에 저장하기
# base_path = 'exchange_data'

# import csv
# 2025-11-17-11.csv
import csv
from datetime import datetime

# 폴더 만들기
base_path = 'exchange_data'
os.makedirs(base_path, exist_ok=True)

# 1. 파일명 생성
filename = datetime.now().strftime("%Y-%m-%d-%H") + ".csv"

# 3. CSV 파일로 저장
with open(f"{base_path}/{filename}", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(exchange_list)

print(f"{filename} 파일 저장 완료!")