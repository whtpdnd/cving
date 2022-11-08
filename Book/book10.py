import requests 
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn.linear_model import LinearRegression
import datetime as dt
import statsmodels.api as sm
import statsmodels.formula.api as smf

# [함수시작] ========================================
def GetURL(code) :
    
    url  = "https://finance.naver.com/item/sise_day.nhn?code=" + code
    
    agent_head = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    
    response = requests.get(url,headers=agent_head)
    
    soap = BeautifulSoup(response.text, "lxml")
    
    ## table중에서 Class가 "Nnavi"인 것을 탐색
    table_navi = soap.find("table", class_ ="Nnavi")
                           
    ## Class가 "Nnavi"인 Table 중에서 Class가 "pgRR"인 td 태그를 탐색) 
    td_navi = table_navi.find("td", class_="pgRR") 

    ## 탐색한 td 중에서 a태그를 탐색하여 그중에서 "href" 내용을 가지고 옴 
    page_last = td_navi.a.get("href") 

    # 마지막 페이번호를 추출하여 정수로 저장
    page_last = int(page_last.split("&")[1].split("=")[1]) 
    
    #print("마지막 페이지 번호 : " , page_last)
    
    #1 ~ 마지막 페이지를 돌면서 데이터를 수집한다.
    page_last = page_last + 1
    
    for pageno in range(1,page_last) :
        url = "https://finance.naver.com/item/sise_day.nhn?code=" + code + "&page=" + str(pageno)
        print(url)
        response = requests.get(url,headers=agent_head)
        
        ## 요청한 url 중 table 정보를 읽어옴
        table = pd.read_html(response.text) 
        
        #1번째 테이블이 주가 정보임
        if( pageno == 1) :
            data = table[0]
        else:
            data = pd.concat([data, table[0]])
            
        #주가정보가 없는 데이터를 제거
        data = data.dropna()            
        
        #print(data)
        #print("============================================")
    
    #csv 파일로 저장한다.
    filename = code + ".csv"
    data.to_csv(filename,encoding="euc-kr")
    return code
# [함수종료] ========================================

# [함수시작] ========================================
def ReadCSV(code) :
    #CSV 읽기
    df = pd.read_csv(code + ".csv",encoding="euc-kr")
    #print(df.head);
    #print("===========================================\n")
    
    #일련번호 열 삭제
    df.drop(df.columns[0],axis=1,inplace=True)
    #print(df.head);
    #print("===========================================\n")
    
    #print(df.head);
    #print("===========================================\n")
    
    """
    start_datefrom = datetime.datetime.strftime(datetime.datetime(year=2018, month=7, day=12), '%Y.%m.%d')
    df=df.loc[df["날짜"]>start_datefrom]
    
    print(df.head);
    print("===========================================\n")
    """
    
    #날짜를 문자열에서 날짜로 변환
    df["날짜"] =  pd.to_datetime(df["날짜"])
    
    
    #날짜순으로 정렬한다.
    df["일련번호"] = df.sort_index(ascending=False).index + 1
    #print(df["일련번호"]);
    #print("===========================================\n")
    
    #전체 갯수를 얻는다.
    maxrow = df["일련번호"].count()
    #print("전체 행갯수 :", maxrow)
    
    return df;
    
# [함수종료] ========================================

# [함수시작] ========================================
def DrawPlot(df,title) :
    #주가 그리기
    #그래프 크기 설정
    plt.figure(figsize=(10,4))
    
    #한글 설정 
    rc('font', family='Malgun Gothic')
    
    plt.plot(df["날짜"],df["시가"], label="시가")
    plt.plot(df["날짜"],df["종가"], label="종가")
    plt.xlabel("날짜")
    plt.ylabel("주가")
    plt.legend()
    plt.title(title)
    plt.show()    
    plt.close()
    return
# [함수종료] ========================================

# [함수시작] ========================================
#회귀분석을 통한 주가 예측  
def PredictStockA(df,beginVal) :
    #상위 80%를 훈련데이터로 설정한다.
    maxrow = df["시가"].count()
    baserow = maxrow - int(maxrow * 0.8);
    #print("전체 행갯수 :", maxrow)
    #print("기준 행갯수 :", baserow)
    
    #훈련 데이터 얻기 (과거데이터)
    train_data = df.iloc[baserow:][["시가", "종가", "날짜"]]
    #print(train_data)
    
    
    #테스트 데이터 얻기 (최신데이터)
    test_data = df.iloc[0:baserow][["시가", "종가", "날짜"]]
    #print(test_data)
    
    #DrawPlot(train_data,"주가 - 훈련데이터")
    #DrawPlot(test_data,"주가 - 시험데이터")
    
    #훈련데이터와 테스트 테이터의 날짜를 숫자로 변환
    #train_data["날짜"] = train_data["날짜"].map(dt.datetime.toordinal)
    #test_data["날짜"] = test_data["날짜"].map(dt.datetime.toordinal)
    
    #단순회귀분석 모형 객체 생성
    lr = LinearRegression()
    
    #독립 변수 X
    x = train_data[["시가"]]
    print(x)
    
    #종속 변수 Y
    y = train_data["종가"]
    print(y)
    
    #훈련데이터로 모형 학습
    #lr.fit(train_data,train_data["시가"])
    lr.fit(x,y)
    
    # 모형에 테스트 데이터를 입력하여 예측한 값 y_predict 를 얻는다.
    p = test_data[["시가"]]
    print(p)
    y_predict = lr.predict(p)
    
    #시리즈로 변환
    y_predict = pd.Series(y_predict)
    test_data["예측"] = y_predict
    test_data["예측"] = test_data["예측"].astype("int64")
    
    """
    for item in test_data["시가"]:
        print("시가:", item)
        
    for item in test_data["종가"]:
        print("종가:", item)    
    
    #print(y_predict)
    for item in y_predict:
        print("예측:", item)
    """
    
    #주가 그리기
    #그래프 크기 설정
    plt.figure(figsize=(10,4))
    
    #한글 설정 
    plt.rc('font', family='Malgun Gothic')
    
    plt.plot(test_data["날짜"],test_data["시가"], label="시가")
    plt.plot(test_data["날짜"],test_data["종가"], label="종가")
    plt.plot(test_data["날짜"],test_data["예측"], label="예측")
    
    plt.xlabel("날짜")
    plt.ylabel("주가")
    plt.legend()
    plt.title("주가예측")
    plt.show()    
    plt.close()
    
    #오늘의 시가를 이용하여 예측한다.
    y_predict = lr.predict([[beginVal]])
    #print(y_predict)
    
    #예측된 자료를 리턴한다.
    return y_predict[0]

# [함수종료] ========================================

# [함수시작] ========================================
#다항 회귀분석을 통한 주가 예측  
def PredictStockB(df,beginVal) :
    #상위 80%를 훈련데이터로 설정한다.
    maxrow = df["시가"].count()
    baserow = maxrow - int(maxrow * 0.8);
    #print("전체 행갯수 :", maxrow)
    #print("기준 행갯수 :", baserow)
    
    #기준가=종가 * 종가
    df["기준가"] = df["종가"] * df["종가"]
    
    #훈련 데이터 얻기 (과거데이터)
    train_data = df.loc[baserow:][["시가", "종가", "기준가", "날짜"]]
    #print(train_data)
    
    
    #테스트 데이터 얻기 (최신데이터)
    test_data = df.loc[:baserow][["시가", "종가", "기준가", "날짜"]]
    #print(test_data)
    
    #DrawPlot(train_data,"주가 - 훈련데이터")
    #DrawPlot(test_data,"주가 - 시험데이터")
    
    #훈련데이터와 테스트 테이터의 날짜를 숫자로 변환
    #train_data["날짜"] = train_data["날짜"].map(dt.datetime.toordinal)
    #test_data["날짜"] = test_data["날짜"].map(dt.datetime.toordinal) 
    
    #독립 변수 X
    x = train_data[["시가","기준가"]]
    
    #종속 변수 Y
    y = train_data["종가"]
 
    ## 회귀분석 수행
    mod = sm.OLS(x, y)
    res = mod.fit()
    
    # 모형에 테스트 데이터를 입력하여 예측한 값 y_predict 를 얻는다.
    p = test_data[["시가"]]
    y_predict = res.predict(p)
    
    #시리즈로 변환
    y_predict = pd.Series(y_predict[0])
    #print(y_predict)    
    test_data["예측"] = y_predict
    test_data["예측"] = test_data["예측"].astype("int64")
    
    """
    for item in test_data["시가"]:
        print("시가:", item)
        
    for item in test_data["종가"]:
        print("종가:", item)    
    
    #print(y_predict)
    for item in y_predict:
        print("예측:", item)
    """
    
    #주가 그리기
    #그래프 크기 설정
    plt.figure(figsize=(10,4))
    
    #한글 설정 
    plt.rc('font', family='Malgun Gothic')
    
    plt.plot(test_data["날짜"],test_data["시가"], label="시가")
    plt.plot(test_data["날짜"],test_data["종가"], label="종가")
    plt.plot(test_data["날짜"],test_data["예측"], label="예측")
    
    plt.xlabel("날짜")
    plt.ylabel("주가")
    plt.legend()
    plt.title("주가예측")
    plt.show()    
    plt.close()

    #오늘의 시가를 이용하여 예측한다.
    p = [[beginVal]]
    y_predict = res.predict(p)
    #print(y_predict[0][0])

    return y_predict[0][0]

    
# [함수종료] ========================================    

#삼성전자 
code = "005930"
#시가
begin = 58900

#GetURL(code)

df = ReadCSV(code)

#특정 날짜 이후 데이터만 추출한다.
cutdate = dt.datetime.strftime(dt.datetime(year=1990, month=1, day=1), '%Y.%m.%d')
df = df.loc[df["날짜"] > cutdate]

DrawPlot(df,"주가")

p = PredictStockA(df,begin)
print("예측종가 :" , int(p))


p = PredictStockB(df,begin)
print("예측종가 :" , int(p))

