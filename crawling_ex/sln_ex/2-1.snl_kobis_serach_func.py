# 1. 필요한 라이브러리 로딩
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time  

# 파일저장 함수를 정의한 모듈 로딩
from my_lib import save_lib 


# 2. 크롬브라우저 옵션 정의
options = webdriver.ChromeOptions()             # 옵션 설정 객체 생성
options.add_argument("window-size=1000,1000")   # 브라우저 크기 설정(가로 x 세로)
options.add_argument("--no-sandbox")              # 샌드박스 사용 안하겠다. 텝별로 분리하겠다. 
options.add_argument("--disable-dev-shm-usage")  # 메모리 부족 방지
# options.add_argument("headless")              # 크롬 창을 안뜨게함.
# options.add_experimental_option("excludeSwitches", ["enable-logging"])


# 3. 크롬 웹드라이브을 통한 크롬브라우저 객체 생성
# 방법1 자동으로 다운로드(현재 크롬 브라우저 버전에 맞게 )
# ChromeDriver 경로를 지정하는 Service 객체 생성
# service = Service(ChromeDriverManager().install())

# 방법2 방법1이 안될때 메뉴얼하게 다운로드받아서 지정해야함.
# 로컬에 다운로드한 chromedriver.exe 경로 지정
# 다운로드 사이트 : https://googlechromelabs.github.io/chrome-for-testing/
# 메뉴얼하게 지정하는 방법
service = Service("chromedriver_142/chromedriver.exe")

# 크롬 브라우저 객체 생성됨, chrome은 브라우저 객체 식별자
chrome = webdriver.Chrome(service=service, options=options) 

# 4. 데이터 수집할 웹 주소
url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"

chrome.get(url)
time.sleep(0.5)

# 지정한 요소가 브라우저에 로딩될때까지 기다림, 최대 10초
wait = WebDriverWait(chrome, 10) 
def find(wait, css_selector):
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

# 5. 데이터 수집할 부분에 대한 검색 액션 수행
try:
    ## 한국 영화만 선택, 해외 체크박스 해제 액션
    # 셀렉터 지정방법
    # ul.list_idx li input#repNationNoKor  또는
    # ul.list_idx li label[for='repNationNoKor']
    # find(wait, "셀렉터")
    # 지정 셀렉터 요소가 로딩될때까지 기다리고, 로딩되면 요소 리턴
    # ele = find(wait, "ul.list_idx li input#repNationNoKor")
    # ele = find(wait, "input#repNationNoKor")
    ele = find(wait, "label[for='repNationNoKor']")
    ele.click()

    # 로딩된 요소 클릭
    btn = find(wait, ".wrap_btn button.btn_blue")
    btn.click()

    # 조회된 데이터에서 필요한 데이터 수집
    # 각영화데이터를 list로 추출(tbody tr 을 목록으로 추출 )
    time.sleep(0.5) # 클롤링할 데이터 요소가 로딩될때까지 잠기 기다리기
    # "table.tbl_comm tbody tr" 해당 셀렉터의 모든 요소를 추출함
    items = chrome.find_elements(By.CSS_SELECTOR, "table.tbl_comm tbody tr")
    # print(items)
    print("영화제목 | 개봉일 | 예매매출액 | 예매관람수")
    movie_lists = []
    for item in items:
        # 하나의 tr 안에서 td가 두번째인 요소의 텍스트 추출
        title = item.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()
        # 하나의 tr 안에서 td가 세번째인 요소의 텍스트 추출
        open_date = item.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()
        # open_date가 없는 경우 처리
        if not open_date:
           open_date = "-"
        # 예매매출액
        reserve_sales= item.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip()
        # 예매관객수
        reserve_viewers = item.find_element(By.CSS_SELECTOR, "td:nth-child(7)").text.strip()
        # print(f"{title} | {open_date} | {reserve_sales} | {reserve_sales}")
        movie_lists.append([title, open_date, reserve_sales, reserve_sales])
    print(movie_lists)
    print("-"*30)

    # 조회버튼 로딩되면 클릭하기
    # btn = find(wait, "")
    # time.sleep()

except Exception as e:
   print("오류", e)

# 파일로 저장하기(csv)
# 6. 리스트 -> 파일에 저장
# 현재 날짜/시간 가져오기

# 호출부
data_keyword = "movie"
head = ["영화제목","개봉일", "예매매출액", "예매관람수"]
save_lib.save_datas(data_keyword, head, movie_lists)

# print("-"*30)
chrome.close() # tab 모두 종료
chrome.quit() # tab 모두 종료

