import pymysql
def check_upload(email):
    conn=pymysql.connect(host='localhost',user='root',passwd='',port=3306,db='hospital',autocommit=True)
    cur=conn.cursor()
    sql="select * from photodata where email='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    photo="not"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    return photo
