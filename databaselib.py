import pymysql
def getdbcur():
    conn=pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         passwd='',
                         db='hospital',
                         autocommit=True)
    cur=conn.cursor()
    return cur