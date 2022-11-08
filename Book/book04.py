import requests
from bs4 import BeautifulSoup

mURL = "https://www.donga.com/news/Economy/article/all/20221024/116115198/1"
response = requests.get(mURL)
print(response.text)
print("=" * 30)

soup = BeautifulSoup(response.text, "html.parser")

content = soup.select("div.article_txt")
textAll = ""
for item in content:
    text = item.getText()
    textAll += text
print(textAll)
print("=" * 30)

from konlpy.tag import Okt

#형태소 분석을 시작한다. 
Okt = Okt()

#형태소 분석 (명사)
nouns = Okt.nouns(textAll)
print(nouns)

#한글자는 제거 
for i,v in enumerate(nouns):
    if len(v) < 2:
        nouns.pop(i)
print(nouns)

#명사 빈도 계산
from collections import Counter
count = Counter(nouns)
nouns = count.most_common(50)
print(nouns)
print(type(nouns))


#판다스에서 튜플을 변환
words = []
count = []
for idx,(k,v) in enumerate(nouns) :
    words.append(k)
    count.append(v)
    
print(words)
print("=" * 30)    
print(count)
print("=" * 30)

import pandas as pd
#데이터프레임으로 변환 
nouns = [words,count]
df = pd.DataFrame(nouns)
df = df.transpose()
df.columns  = [ "단어", "빈도수"]
print(df.head())
print("=" * 30)

#빈도수를 숫자로 변환
df["빈도수"] = df["빈도수"].astype("int64")

#단어로 정렬
df = df.sort_values("단어")

import matplotlib.pyplot as plt
from matplotlib import rc

#한글 설정 
rc('font', family='Malgun Gothic')

#단어별 시각화
plt.figure(figsize=(20,10))
plt.plot(df["단어"],df["빈도수"], label="빈도수")
plt.legend()
plt.title("단어별 빈도")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

from wordcloud import WordCloud

#워드 클라우드 표시용 딕셔너리로 변환
wordlist = {}
for i in range(0,df["단어"].count()):
    print(df["단어"][i])
    print(df["빈도수"][i])
    wordlist[df["단어"][i]] = df["빈도수"][i]
print(wordlist)    
print("=" * 30)

#워드 클라우드 표시
wordcloud = WordCloud(font_path = 'HANYGO230.ttf',
                      relative_scaling = 0.5,
                      background_color='white',
                      )
wordcloud.generate_from_frequencies(wordlist)
plt.figure(figsize=(20,10))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()





    
