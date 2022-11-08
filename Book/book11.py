#설치방법 
#pip install snscrape
#pip install twitter
#참고 : https://shlee1990.tistory.com/1077

import twitter
import snscrape
import snscrape.modules.twitter as sw
import warnings
import pandas as pd

import requests
import nltk
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
from urllib.parse import quote
from konlpy.tag import Okt
from matplotlib import rc
from wordcloud import WordCloud
from nltk import word_tokenize
from collections import Counter


#warnings.filterwarnings(action="ignore")

#twttername : 계정명
#startDay : yyyy-mm-dd
#endDay : yyyy-mm-dd
def read_data(twitterName,startDay,endDay) :
    list = []
    df = pd.DataFrame(columns=["URL","DateTime","User ID","Content","UserName"])
    if pd.isnull(twitterName) or twitterName == "" :
        print("error user name")
        return df
    
    #for i,tweet in enumerate(sw.TwitterSearchScraper("from:" + twitterName + " since:" + startDay + " util:" + endDay).get_items()):
    #for i,tweet in enumerate(sw.TwitterSearchScraper("from:ARMY52Hz").get_items()):
    for i,tweet in enumerate(sw.TwitterSearchScraper("올림픽  since:2020-07-01 until:2020-08-02").get_items()):
        if i > 10 :
            break
        list.append([tweet.url, tweet.date, tweet.id, tweet.content, tweet.username])
        df = pd.DataFrame(list,columns=["URL","DateTime","User ID","Content","UserName"])
    return df

df = read_data("ARMY52Hz","2021-07-01","2021-08-03")
print(df["Content"])

#df2 = df["Content"]
#df2.to_csv("twitter.csv")

# \xa0, \xa9 를 없애줌
#df = df.applymap(lambda x: x.replace('\xa0','').replace('\xa9',''))  
#df["Content"] = df["Content"].replace('\xa0','').replace('\xa9','')  

df.to_csv("twitter.csv")
"""
for item in df["Content"] :
    print(item)
    print("==============================")
"""

textAll = ""
for item in df["Content"] :
    textAll += item
    textAll += "\n"

#print(textAll) 

#형태소 분석을 시작한다. ========================================
Okt = Okt()

#형태소 분석 (명사)
nouns = Okt.nouns(textAll)
#print(nouns)
#print(type(nouns))

nouns_list = []

#한글자는 제거 
for i,v in enumerate(nouns):
    print("V=", v, "len:", len(v))
    if len(v) >= 2:
        nouns_list.append(nouns[i])
        
nouns = nouns_list
        
#print("-----------------------------------")        
for i,v in enumerate(nouns):
    print("V=", v, "len:", len(v))
        
#명사 빈도 계산
count = Counter(nouns)
nouns = count.most_common(100)
#print(nouns)
#print(type(nouns))

#판다스에서 튜플을 변환
words = []
count = []
for item in nouns :
    if( item[0] != "올림픽") :
        words.append(item[0])
        count.append(item[1])

#print(words)    
#print(count)
nouns = [words,count]
#print(nouns)
df = pd.DataFrame(nouns)
df = df.transpose()
df.columns  = [ "단어", "빈도수"]
#빈도수를 숫자로 변환
df["빈도수"] = df["빈도수"].astype("int64")
#print(df)

#단어로 정렬
df = df.sort_values("단어")
#print(df)

#한글 설정 
rc('font', family='Malgun Gothic')

#워드 클라우드 표시용 딕셔너리로 변환
wordlist = {}
for i in range(0,df["단어"].count()):
    print(df["단어"][i])
    print(df["빈도수"][i])
    wordlist[df["단어"][i]] = df["빈도수"][i]
#print(wordlist)    

#워드 클라우드 표시 ========================================
wordcloud = WordCloud(font_path = 'HANYGO230.ttf',
                      relative_scaling = 0.5,
                      background_color='white',
                      );
wordcloud.generate_from_frequencies(wordlist)
plt.figure(figsize=(20,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()



   