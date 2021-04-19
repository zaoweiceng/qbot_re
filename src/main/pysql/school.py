import pymysql
import sys
import json

fp = open('./config', encoding='utf8')
fp_text = fp.read()
project_src = json.loads(fp_text)
if project_src['local_project_dir'] != '':
    sys.path.append(project_src['local_project_dir'])

import src.main.utils.option as option

OPT = option.get_sql_info()
db = pymysql.connect(host=OPT['host'], user=OPT['user'], passwd=OPT['password'], db=OPT['db'], port=OPT['port'],
                         charset='utf8')
'''
插入数据                 insert_all(no, password, qqno)   返回Ture或False
根据qqno更新nopassword   update_nopassword_by_qqno        返回Ture或False
根据qqno删除数据          delete_by_qqno(qqno)             返回Ture或False
根据qqno查询nopassword   find_nopassword_by_qqno(qqno)    返回nos[]和passwords[]
查询所有数据              find_all()                       返回nos[]和passwords[]和qqnos[]
'''


def insert_all(no, password, qqno):
    flag = True
    cursor = db.cursor()
    sql = """INSERT INTO stulogin(no,password,qqno)VALUES(%s,%s,%s)"""
    sqlargs = []
    sqlargs.append(no)
    sqlargs.append(password)
    sqlargs.append(qqno)
    try:
        cursor.execute(query=sql, args=sqlargs)
        print('执行sql语句')
        # 提交到数据库执行
        db.commit()
        print('提交数据库')
    except:
        db.rollback()
        print('错误')
        flag = False
    cursor.close()
    return flag


def update_nopassword_by_qqno(no, password, qqno):
    flag = True
    cursor = db.cursor()
    sql = """UPDATE stulogin SET no=%s, password=%s WHERE qqno=%s"""
    sqlargs = []
    sqlargs.append(no)
    sqlargs.append(password)
    sqlargs.append(qqno)
    try:
        cursor.execute(query=sql, args=sqlargs)
        print('执行sql语句')
        # 提交到数据库执行
        db.commit()
        print('提交数据库')
    except:
        db.rollback()
        print('错误')
        flag = False
    cursor.close()
    return flag


def delete_by_qqno(qqno):
    flag = True
    cursor = db.cursor()
    sql = """DELETE FROM stulogin WHERE qqno=%s"""
    sqlargs = []
    sqlargs.append(qqno)
    try:
        cursor.execute(query=sql, args=sqlargs)
        print('执行sql语句')
        # 提交到数据库执行
        db.commit()
        print('提交数据库')
    except:
        db.rollback()
        print('错误')
        flag = False
    cursor.close()
    return flag


def find_nopassword_by_qqno(qqno):
    flag = True
    cursor = db.cursor()
    sql = """SELECT * FROM stulogin WHERE qqno=%s"""
    sqlargs = []
    sqlargs.append(qqno)
    nos = []
    passwords = []
    try:
        cursor.execute(query=sql, args=sqlargs)
        print('执行sql语句')
        results = cursor.fetchall()
        for row in results:
            nos.append(row[0])
            passwords.append(row[1])
    except:
        print('错误')
        flag = False
    cursor.close()
    if len(nos) == 0:
        flag = False
        return [flag, "", ""]
    else:
        return [flag, nos[0], passwords[0]]


def find_all():
    flag = True
    cursor = db.cursor()
    sql = """SELECT * FROM stulogin"""
    nos = []
    passwords = []
    qqnos = []
    try:
        cursor.execute(query=sql)
        print('执行sql语句')
        results = cursor.fetchall()
        for row in results:
            nos.append(row[0])
            passwords.append(row[1])
            qqnos.append(row[2])
    except:
        print('错误')
        flag = False
    cursor.close()
    if len(nos) == 0:
        flag = False
        return [flag, "", "", ""]
    else:
        return [flag, nos[0], passwords[0], qqnos[0]]

