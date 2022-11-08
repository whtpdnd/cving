"""
pip install selenium
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver_name = "D:/chromedriver/chromedriver.exe"

driver = webdriver.Chrome(executable_path=driver_name)

url = "https://finance.naver.com/item/sise_day.nhn?code=005930"

driver.get(url)

time.sleep(2)

html = driver.page_source

print(html)

soap = BeautifulSoup(html, "lxml")

## table중에서 Class가 "Nnavi"인 것을 탐색
table_navi = soap.find("table", class_ ="Nnavi")
                       
## Class가 "Nnavi"인 Table 중에서 Class가 "pgRR"인 td 태그를 탐색) 
td_navi = table_navi.find("td", class_="pgRR") 

## 탐색한 td 중에서 a태그를 탐색하여 그중에서 "href" 내용을 가지고 옴 
page_last = td_navi.a.get("href") 

# 마지막 페이번호를 추출하여 정수로 저장
page_last = int(page_last.split("&")[1].split("=")[1]) 

print("마지막 페이지 번호 : " , page_last)








