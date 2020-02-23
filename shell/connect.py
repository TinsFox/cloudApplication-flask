"""
    Created by TinsFox on 2020-02-19.
"""

__author__ = 'TinsFox'

import pymysql

# 打开数据库连接
db = pymysql.connect(host='hk.tinsfox.com', port=3306,
                     user='root', passwd='d@FieF93a28G', db='cloudApplication', charset='utf8')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print("Database version : %s " % data)

# 关闭游标
cursor.close()
# 关闭数据库连接
db.close()