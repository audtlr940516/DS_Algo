#!/usr/bin/env python
# coding: utf-8




###################################################################
#                                                                 #
#   2026 DS2 Database Project : Recommendation using SQL-Python   #
#                                                                 #
###################################################################








import mysql.connector
from tabulate import tabulate
import pandas as pd
import math
import sys
import os




BASE_DIR = os.path.dirname(os.path.abspath(__file__))




## Connect to Remote Database
## Insert database information




HOST = "astronaut.snu.ac.kr"
USER = "DS2026_00031"
PASSWD = "DS2026_00031"
DB = "DS2026_00031"




connection = mysql.connector.connect(
    host=HOST,
    port=7000,
    user=USER,
    passwd=PASSWD,
    db=DB,
    autocommit=True,  # to create table permanently
)




cur = connection.cursor(dictionary=True)








## 수정할 필요 없는 함수입니다.
# DO NOT CHANGE INITIAL TABLES IN prj.sql
def get_dump(mysql_con, filename):
    """
    connect to mysql server using mysql_connector
    load .sql file (filename) to get queries that create tables in an existing database (fma)
    """
    query = ""
    try:
        with mysql_con.cursor() as cursor:
            for line in open(filename, "r"):
                if line.strip():
                    line = line.strip()
                    if line[-1] == ";":
                        query += line
                        cursor.execute(query)
                        query = ""
                    else:
                        query += line




    except Warning as warn:
        print(warn)
        sys.exit()



## 수정할 필요 없는 함수입니다.
# SQL query 를 받아 해당 query를 보내고 그 결과 값을 dataframe으로 저장해 return 해주는 함수
def get_output(query):
    cur.execute(query)
    out = cur.fetchall()
    df = pd.DataFrame(out)
    return df

# [Algorithm 1] Popularity-based Recommendation - 1 : Popularity by rating count
def popularity_based_count():
    user = int(input("User Id: "))
    rec_num = int(input("Number of recommendations?: "))

    print(f"Popularity Count based recommendation")
    print("=" * 99)

    # TODO: remove sample, return actual recommendation result as df
    # YOUR CODE GOES HERE !
    # 쿼리의 결과를 results 변수에 저장하세요.

    query = f"""SELECT item , count(rating) as prediction
               FROM ratings
               WHERE item NOT IN (SELECT item
                                     FROM ratings
                                     WHERE `user` = {user} and rating is NOT NULL)
               GROUP BY item
               ORDER BY prediction desc , item asc
               LIMIT {rec_num};

    """
    cur.execute(query)
    results = [(row['item'],row['prediction']) for row in cur.fetchall()]
   
    # 최종 결과 얻은 뒤, 중간 계산 중 만든 table 삭제
    # TODO end




    # Do not change this part
    # do not change column names
    df = pd.DataFrame(results, columns=["item", "prediction"])
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)
    with open("pbc.txt", "w") as f:
        f.write(tab)
    print("Output printed in pbc.txt")








# [Algorithm 2] Popularity-based Recommendation - 2 : Popularity by average rating
def popularity_based_rating():
    user = int(input("User Id: "))
    rec_num = int(input("Number of recommendations?: "))




    print(f"Popularity Rating based recommendation")
    print("=" * 99)




    # TODO: remove sample, return actual recommendation result as df
    # YOUR CODE GOES HERE !




    # 1. 평균 평점이 높은 아이템들을 추천하도록
    # 2. 알고리즘 1과 동일하게  item prediction 으로 항목 추천
    # 3. 평점 보정 작업 필요 - 최저 평점 0 , 최고 평점 1 로 환산
    #                 보정 평점 (P) = [ 실제 평점 - min(r) ] / [ max(r) - min(r) ]
    #                 1개만 평가했을 경우 min(r) = 0 으로 계산
    # 4. 소수점 넷째자리 까지 보정

    query = f"""SELECT new_rating__table.item , ROUND ( AVG( change_rating ) ,4) as prediction
                FROM ( SELECT  rat.item , rat.`user` , ROUND (CASE WHEN   max_rating  = min_rating   THEN  1
                                                              ELSE  (rat.rating - min_rating ) / (max_rating - min_rating)
                                                              END , 4)
                                                              AS change_rating
                       FROM  ratings  rat
                             join ( SELECT ratings.`user` , CASE WHEN  count(rating) = 1  THEN 0
                                                            ELSE MIN(rating)
                                                            END    
                                                            AS min_rating ,
                                           MAX(rating) as max_rating
                                    FROM ratings
                                    WHERE rating is not NULL
                                    GROUP BY  ratings.`user` )  AS  min_max_table ON rat.`user` = min_max_table.`user`
                       WHERE  rating is not NULL ) AS  new_rating__table
                WHERE new_rating__table.change_rating is not NULL and new_rating__table.item not in (SELECT item FROM ratings WHERE `user` = {user} AND rating IS NOT NULL)
                group by new_rating__table.item
                ORDER BY prediction desc  ,  new_rating__table.item  asc
                LIMIT {rec_num};
    """
    cur.execute(query)
    results = [(row['item'],row['prediction']) for row in cur.fetchall()]


    # 최종 결과 얻은 뒤, 중간 계산 중 만든 table 삭제
    # TODO end

    # Do not change this part
    # do not change column names
    df = pd.DataFrame(results, columns=["item", "prediction"])
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)
    with open("pbr.txt", "w") as f:
        f.write(tab)
    print("Output printed in pbr.txt")




# [Algorithm 3] User-based Recommendation
def ubcf():
    user = int(input("User Id: "))
    rec_num = float(input("Recommendation Threshold: "))


    print("=" * 99)
    print(f"User-based Collaborative Filtering")
    print(f"Recommendations for user {user}")

    # TODO: remove sample, return actual recommendation result as df
    # YOUR CODE GOES HERE !
    # 쿼리의 결과를 results 변수에 저장하세요.


    cur.execute("DROP TABLE IF EXISTS new_rating__table")
    cur.execute("DROP TABLE IF EXISTS similarity_between")
    cur.execute("DROP TABLE IF EXISTS normal_similarity_between")


    query = f"""CREATE TABLE  new_rating__table   AS


                SELECT    rat.`user` , rat.item ,  ROUND (CASE WHEN  max_rating  = min_rating   THEN  1
                                                          ELSE   (rat.rating - min_rating ) / (max_rating - min_rating)
                                                          END  ,  4 )   AS change_rating
                FROM    ratings rat  
                    JOIN  ( SELECT ratings.`user` , CASE WHEN  count(rating) = 1  THEN 0
                                                    ELSE MIN(rating)
                                                    END    AS min_rating ,
                                   MAX(rating) as max_rating
                            FROM ratings
                            WHERE rating is not NULL
                            GROUP BY   ratings.`user` )  AS  min_max_table ON rat.`user` = min_max_table.`user`
                where  rat.rating is not NULL ;
    """
    cur.execute(query)


    query = f"""CREATE TABLE  similarity_between   AS


                SELECT user_1 , user_2 , sim , sim_rank
                FROM    ( SELECT us.user_1 , us.user_2 , us.sim , ROW_NUMBER() OVER ( PARTITION BY us.`user_1` ORDER BY sim desc , us.user_2 asc)  AS sim_rank
                          FROM user_similarity us
                          WHERE us.user_1 = {user}
                        ) AS ranked_sim
                WHERE sim_rank <= 5
    """
    cur.execute(query)


    query = f"""CREATE TABLE  normal_similarity_between   AS


                SELECT user_1 , user_2 , ROUND (  sim / SUM(sim) OVER() , 4)
                                                AS change_similarity  , sim_rank
                FROM    similarity_between
    """
    cur.execute(query)


    query = f""" SELECT item , ROUND ( SUM(change_rating * change_similarity) , 4) AS prediction
                 FROM normal_similarity_between JOIN new_rating__table ON normal_similarity_between.user_2 = new_rating__table.`user`
                 WHERE item NOT IN (SELECT item FROM ratings WHERE `user` = {user} AND rating is NOT NULL )
                 GROUP BY item
                 HAVING prediction >= {rec_num}
                 ORDER BY prediction desc , item asc;
    """
    cur.execute(query)


    results = [(row['item'],row['prediction']) for row in cur.fetchall()]
   
    cur.execute("DROP TABLE IF EXISTS similarity_between")
    cur.execute("DROP TABLE IF EXISTS new_rating__table")
    cur.execute("DROP TABLE IF EXISTS normal_similarity_between")

    # 최종 결과 얻은 뒤, 중간 계산 중 만든 table 삭제
    # TODO end

    # Do not change this part
    # do not change column names
    df = pd.DataFrame(results, columns=["item", "prediction"])
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)
    with open("ubcf.txt", "w") as f:
        f.write(tab)
    print("Output printed in ubcf.txt")


# [Algorithm 4] (Optional) User similarity
def user_similarity():

    print("=" * 99)
    print(f"User similarity")

    # TODO: remove sample, return actual recommendation result as df
    # YOUR CODE GOES HERE !

    cur.execute("DROP TABLE IF EXISTS my_user_similarity")
    cur.execute("DROP TABLE IF EXISTS my_user_similarity_1")   
    cur.execute("DROP TABLE IF EXISTS my_user_similarity_2")               
    cur.execute("DROP TABLE IF EXISTS my_user_similarity_3")   

    # 1. rating 항목 -> 전치행렬 곱
    # 2. 유저 별로, 아이템 평점의 제곱 합의 제곱근

    query = f"""CREATE TABLE  my_user_similarity_1   AS

        SELECT ra1.`user` AS user_1 , ra2.`user` AS user_2 , SUM(ra1.rating * ra2.rating) AS rating_do
        FROM ratings ra1 JOIN ratings ra2 on ra1.item = ra2.item
        WHERE ra1.rating is NOT NULL AND ra2.rating is NOT NULL
        GROUP BY ra1.`user` , ra2.`user`

    """
    cur.execute(query)

    query = f"""CREATE TABLE  my_user_similarity_2   AS
            
        SELECT user_1 , user_2 , SQRT(rating_do) AS rating_sq
        FROM my_user_similarity_1 
        WHERE user_1 = user_2

    """
    cur.execute(query)

    query = f"""CREATE TABLE  my_user_similarity_3   AS
            
        SELECT MU1.user_1 AS user_01 , MU2.user_1 AS user_02 , MU1.rating_sq * MU2.rating_sq AS rating_sq2
        FROM my_user_similarity_2 AS MU1 JOIN my_user_similarity_2 AS MU2

    """
    cur.execute(query)

    query = f"""CREATE TABLE  my_user_similarity   AS
            
        SELECT TA1.user_1 , TA1.user_2 , CASE WHEN 
                                                 TA1.user_1 != TA1.user_2   THEN 
                                                                            ROUND ( TA1.rating_do / TA2.rating_sq2 , 1 ) 
                                            ELSE
                                                0  END 
                                                AS sim
        FROM my_user_similarity_1 AS TA1 JOIN my_user_similarity_3 TA2 ON TA1.user_1 = TA2.user_01 AND TA1.user_2 = TA2.user_02

        ORDER BY TA1.user_1 asc , TA1.user_2 asc 

    """
    cur.execute(query)    


    # 유사도 연산을 직접 구현하여 my_user_similarity 테이블에 저장하세요.
    df = get_output("SELECT * FROM my_user_similarity")
    # 최종 결과 얻은 뒤, 중간 계산 중 만든 table 삭제

    cur.execute("DROP TABLE IF EXISTS my_user_similarity")
    cur.execute("DROP TABLE IF EXISTS my_user_similarity_1")   
    cur.execute("DROP TABLE IF EXISTS my_user_similarity_2")               
    cur.execute("DROP TABLE IF EXISTS my_user_similarity_3")   


    # TODO end

    # Do not change this part
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    # do not print since it is too large
    # print(tab)
    with open("user_similarity.txt", "w") as f:
        f.write(tab)
    print("Output printed in user_similarity.txt")








## 수정할 필요 없는 함수입니다.
# Print and execute menu
def menu():
    print("=" * 99)
    print("0. Initialize")
    print("1. Popularity Count-based Recommendation")
    print("2. Popularity Rating-based Recommendation")
    print("3. User-based Collaborative Filtering")
    print("4. User similarity (Optional)")
    print("5. Connector example")
    print("6. Exit database")
    print("=" * 99)




    while True:
        m = int(input("Select your action : "))
        if m < 0 or m > 6:
            print("Wrong input. Enter again.")
        else:
            return m








def execute():
    terminated = False
    while not terminated:
        m = menu()
        if m == 0:
            # 수정할 필요 없는 함수입니다.
            # Upload prj.sql before this
            # If autocommit=False, always execute after making cursor
            try:
                file_path = os.path.join(BASE_DIR, 'prj.sql')
                get_dump(connection, file_path)
                print("Database initialized successfully.")
            except:
                print("Error initializing database.")
        elif m == 1:
            popularity_based_count()
        elif m == 2:
            popularity_based_rating()
        elif m == 3:
            ubcf()
        elif m == 4:
            user_similarity()
        elif m == 5:
            # 수정할 필요 없는 함수입니다.
            # mysql connector 사용 방법 예시입니다.
            connector_example()
        elif m == 6:
            terminated = True








def connector_example():
    print("Connector example")
    print("=" * 99)
    rat_num = int(input("Number of rows in ratings?: "))
    sim_num = int(input("Number of rows in similarity?: "))




    query = f"SELECT * FROM ratings LIMIT {rat_num}"
    df = get_output(query)
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)




    query = f"SELECT * FROM user_similarity LIMIT {sim_num}"
    df = get_output(query)
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)




    query = "DROP TABLE IF EXISTS test;"
    df = get_output(query)




    query = "CREATE TABLE test AS SELECT * FROM ratings LIMIT 5;"
    df = get_output(query)




    query = "SELECT * FROM test;"
    df = get_output(query)
    tab = tabulate(df, headers=df.columns, tablefmt="psql", showindex=False)
    print(tab)




    query = "DROP TABLE test;"
    df = get_output(query)








# DO NOT CHANGE
if __name__ == "__main__":
    execute()


