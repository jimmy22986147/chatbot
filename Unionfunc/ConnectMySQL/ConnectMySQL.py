#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import pandas as pd
import numpy as np

class MySqlConnect:
    def __init__(self, host, user, passwd):
        def MySqlLink(self):
            try:
                dbconnect = pymysql.connect(host=self.host,
                                            user=self.user,
                                            passwd=self.passwd,
                                            charset='utf8mb4')
                cur = dbconnect.cursor() ## 使用 cursor() 方法创建一个游标对象 cur
                return dbconnect, cur
            except ConnectionError as e:
                print("数据库连接异常!" + str(e))
        self.host = host#ip
        self.user = user
        self.passwd = passwd   
        dbconnect, cur = MySqlLink(self)
        self.dbconnect = dbconnect
        self.cur = cur

    def MySQLQuery(self, sqlquery):
        self.cur.execute(sqlquery)
        rows = self.cur.fetchall()
        colnames_sqlquery = [i[0] for i in self.cur.description]
        reusltlist = []
        for row in rows:
            reusltlist.append(row)       
        result = pd.DataFrame(reusltlist, columns=colnames_sqlquery)
        return result
    
    def MySQLExemany(self, df, table_name, list_insert):
        def insert_statementstring(list_insert):
            times = len(list_insert)
            if times == 1:
                res1 = '('+ list_insert[0]+ ')'
                res2 = ' VALUES (%s)'
            elif times >= 1:
                res1 = '('+ ','.join(list_insert)+ ')'
                res2 = ' VALUES ('+ '%s,'*(times-1)+ '%s'+')'
            return res1, res2
        row_nuw = df.shape[0]
        listdata = []  
        for i in range(row_nuw):
            row_data = df.iloc[i, :]  # 按row获取df的值
            listdata.append(list(row_data.values))  
        #table_name = 'PastMessageRecord'
        res1, res2 = insert_statementstring(list_insert)

        sql = "INSERT INTO " +table_name + res1 + res2
        self.cur.executemany(sql, listdata)  # 执行SQL语句
        self.dbconnect.commit()
        listdata.clear()
        print('插入成功！' + '共计' + str(row_nuw) + '条数据!')

    def MySQLUpdate(self, updatestring):
        self.cur.execute(updatestring)
        self.dbconnect.commit()