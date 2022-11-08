"""
MySQL 라이브러리 설치 
pip install pymysql
"""

"""
MySQL 원격 접속 허용
create user 'root'@'%' identified by 'ezen';
grant all privileges on  *.* to 'root'@'%';
flush privileges;
"""
"""
create database stock;
use stock;
create table stock (date varchar(20),start int,end int);
"""

import pymysql

con = pymysql.connect(
    host="127.0.0.1",
    port=3306, 
    user="root", 
    passwd="ezen",
    db="stock", charset ="euckr")

if con != None :
    cursor = con.cursor()
else :
    exit(0) 

   
#insert 구문 실행
sql  = "insert into stock (date,start,end) "    
sql += "values ('2022.10.24',10,20) "

cursor.execute(sql)
con.commit()


#select 구문 실행
sql = "select date,start,end from stock "
cursor.execute(sql)

num_fields = len(cursor.description)
print("컬럼갯수 : " , num_fields)
for name in cursor.description:
    print("컬럼정보 : " , name)
    print("컬럼명 : " , name[0])
print("=" * 30)

rows_data = cursor.fetchall()
total = len(rows_data)
print("행갯수 : " , num_fields)
for i in range(0,total) :
    print(rows_data[i])
    print("=" * 30)

for i in range(0,total) :
    print("date:" , rows_data[i][0])
    print("start:" , rows_data[i][1])
    print("end:" , rows_data[i][2])
    print("=" * 30)

con.close()

