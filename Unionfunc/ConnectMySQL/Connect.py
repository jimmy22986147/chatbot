#批量将Excel数据写入MySQL
import pymysql
import xlrd
import numpy as np
import keyring
#keyring.set_password('MySQL_ConnectToAI', 'jimmyai', 'DADgDaijiMmY46hE*&GT')


def mysql_link(host, user, db_name, form='MySQL_ConnectToAI'):
    try:
        db = pymysql.connect(host=host,
                             user=user,
                             passwd=keyring.get_password(form, user),
                             db=db_name,
                             charset='utf8mb4')
        cur = db.cursor() ## 使用 cursor() 方法创建一个游标对象 cur
        return db, cur
    except ConnectionError as e:
        print("数据库连接异常!" + str(e))

def MySQLExemany(db, cur, df):
    row_nuw = df.shape[0]
    #print(row_nuw - 1)
    listdata = []  
    for i in range(row_nuw):
        row_data = df.iloc[i, :]  # 按row获取df的值
        listdata.append(list(row_data.values))  
    table_name = 'PastMessageRecord'
    sql = "INSERT INTO " + table_name+"(DIALOGUE_CONTENT, QUESTION_TYPE, Complain, ComplainDetail)"+ " VALUES (%s, %s, %s, %s)"
    cur.executemany(sql, listdata)  # 执行SQL语句
    db.commit()
    listdata.clear()
    print('插入成功！' + '共计' + str(row_nuw) + '条数据!')


def MySQLUpdate(db, cur, updatestring):
    cur.execute(updatestring)
    db.commit()


