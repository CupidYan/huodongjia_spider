
# -*- coding: utf-8 -*- #

import MySQLdb

def InsertData(TableName,dic):

   try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='88888888',db='test',port=3306)  #链接数据库
    cur=conn.cursor()
    COLstr=''   #列的字段
    ROWstr=''  #行字段

    ColumnStyle=' VARCHAR(20)'
    for key in dic.keys():
         COLstr=COLstr+' '+key+ColumnStyle+','
         ROWstr=(ROWstr+'"%s"'+',')%(dic[key])

    #推断表是否存在，存在运行try。不存在运行except新建表，再insert
    try:
      cur.execute("SELECT * FROM  %s"%(TableName))
      cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))

    except MySQLdb.Error,e:
      cur.execute("CREATE TABLE %s (%s)"%(TableName,COLstr[:-1]))
      cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))
    conn.commit()
    cur.close()
    conn.close()

   except MySQLdb.Error,e:
      print "Mysql Error %d: %s" % (e.args[0], e.args[1])


if __name__=='__main__':
    dic={"a":"b","c":"d"}
    for i in range(12):
     InsertData('testtable',dic)