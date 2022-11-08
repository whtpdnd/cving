import requests
from bs4 import BeautifulSoup
import pandas as pd

#네이버 주식에서 특정 페이지 정보 가져오기 
"""
mURL = "https://finance.naver.com/item/sise_day.naver?code=005930&page=1"

agent_head = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

response = requests.get(mURL,headers=agent_head)

print(response.text)
print("=" * 30)

import pandas as pd

table = pd.read_html(response.text) 
data  = table[0]

#주가정보가 없는 데이터를 제거
data = data.dropna()  
print(data)
"""

def GetStock(PageNo) :
    mURL = "https://finance.naver.com/item/sise_day.naver?code=005930&page=" + str(PageNo)

    agent_head = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    
    response = requests.get(mURL,headers=agent_head)
    return response.text
    
for page in range(1,4) :
    text  = GetStock(page)
    table = pd.read_html(text) 
    #주가정보가 없는 데이터를 제거
    table[0] = table[0].dropna()    
    if page == 1 : 
        data  = table[0]
    else :
        data = pd.concat([data, table[0]])

#주가정보가 없는 데이터를 제거
data = data.dropna()  
print(data)

    






    





