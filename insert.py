import pandas as pd
import pymysql
from DBManager import DBManager 
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 21:52:43 2022

@author: user
"""



df = pd.read_csv("movie_info.csv",encoding="cp949")
idx = df['번호'].index
#print(df)
db = DBManager()
db.DBOpen()
df = df.astype('object')
#print(df.dtypes)
print(df.iloc[1][1])
"""
for i,con in enumerate(idx) :
    sql = ""
    sql += "insert into movie_info(mno,mcode,mtitle,making_year,mopenyear,mscore,mhobby,mtime, "
    sql += "mage,poster,gen_m,gen_w,age_10,age_20,age_30,age_40,age_50,summary) "
    sql += "values('" + str(df.iloc[i][4]) + "','" + str(df.iloc[i][1]) + "','" + str(df.iloc[i][2]) + "',' " + str(df.iloc[i][3]) +"','" + str(df.iloc[i][5]) +"','" + str(df.iloc[i][6]) +"','" + str(df.iloc[i][7]) +"','" + str(df.iloc[i][8]) + "',' " + str(df.iloc[i][9]) +"','" + str(df.iloc[i][10]) +"','" + str(df.iloc[i][11]) + "',' " + str(df.iloc[i][12]) +"','" + str(df.iloc[i][13]) +"','" + str(df.iloc[i][14]) +"','" + str(df.iloc[i][15]) +"',' "  + str(df.iloc[i][16]) +"',\"'" + str(df.iloc[i][17]) +"'\") "
    db.RunSQL(sql)

db.DBClose()
"""


