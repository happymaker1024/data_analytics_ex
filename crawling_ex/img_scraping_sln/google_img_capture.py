# pip install webdriver_manager
# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as BS
import os
import urllib.request

options = webdriver.ChromeOptions()
options.add_argument("window-size=1000,1000")
#options.add_argument("no-sandbox") # 보안 격리를 하지않음.(sandbox는 격리의 의미)
# options.add_argument("headless")  # 크롬창을 안뜨게함.
options.add_experimental_option("excludeSwitches", ["enable-logging"])

options = webdriver.ChromeOptions()
options.add_argument("window-size=1000,1000")
options.add_argument("no-sandbox") 
# options.add_argument("headless")  # 크롬 창을 안뜨게함.
options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options) 

def search_selenium(search_name, search_path, search_limit) :
    #구글 검색 url : https://www.google.com/search?q="cat"&hl=ko&tbm=isch
    url = "https://www.google.com/search?q=" + str(search_name) + "&hl=ko&tbm=isch"
    browser.get(url)
    browser.implicitly_wait(3)
    element = len(browser.find_elements(By.CSS_SELECTOR, "img.YQ4gaf"))
    print("로드된 이미지 개수 : ", element)
    browser.implicitly_wait(2)
    try:
        if not os.path.exists(search_path):
            os.makedirs(search_path)
    except OSError as e:
        if e.errno != e.EXIST:
            print("exist directory " + search_name +"/n" + e )

    images = browser.find_elements(By.CSS_SELECTOR, "div.F0uyec")
    cnt = 1
    for image in images:
        if cnt > search_limit:
            break
        image.click()
        img_url = image.find_element(By.TAG_NAME, 'img').get_attribute('src')
        #urllib.request.urlretrieve(img_url, search_path + search_name + str(cnt) + ".jpg")
        urllib.request.urlretrieve(img_url, search_path + str(cnt) + ".jpg")
        browser.implicitly_wait(0.1)
        cnt += 1
    browser.close()

if __name__ == "__main__" :
    search_name = input("검색하고 싶은 키워드 : ")
    search_limit = int(input("원하는 이미지 수집 개수 : "))
    #base_path = 
    search_path = os.path.dirname(os.path.realpath(__file__)) + "/" + search_name + "/"
    print(search_path)    
    # make sub_dir 
    # os.makedirs(sub_dir) # Execution path
    # search_maybe(search_name, search_limit, search_path)
    search_selenium(search_name, search_path, search_limit)