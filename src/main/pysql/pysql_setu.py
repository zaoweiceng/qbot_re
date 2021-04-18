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

'''
更新数据库      write_db(uid, dir, tag) 返回Ture False
根据uid查dir   find_dir_by_id(uid)     返回dirs[]
根据tag查uid   find_ids_by_tag(tag)    返回ids[]
'''


def write_db(uid, dir, tag):
    flag = True
    if find_tf_by_id(uid):
        flag = update_pic(uid, dir, tag)
    else:
        flag = insert_pic(uid, dir, tag)
    return flag


def find_tf_by_id(uid):
    flag = True
    db = pymysql.connect(host=OPT['host'], user=OPT['user'], passwd=OPT['password'], db=OPT['db'], port=OPT['port'],
                         charset='utf8')
    cursor = db.cursor()
    sql = """SELECT * FROM setupic WHERE uid=%s"""
    sqlargs = []
    ids = []
    sqlargs.append(uid)
    try:
        cursor.execute(query=sql, args=sqlargs)
        print('执行sql语句')
        results = cursor.fetchall()
        for row in results:
            ids.append(row[0])
    except:
        print('sql错误')
    cursor.close()
    db.close()
    if len(ids) == 0:
        flag = False
    return flag


def insert_pic(uid, dir, tag):
    flag = True
    db = pymysql.connect(host=OPT['host'], user=OPT['user'], passwd=OPT['password'], db=OPT['db'], port=OPT['port'],
                         charset='utf8')
    cursor = db.cursor()
    sql = """INSERT INTO setupic(uid,dir,tag)VALUES(%s,%s,%s)"""
    sqlargs = []
    sqlargs.append(uid)
    sqlargs.append(dir)
    sqlargs.append(tag)
    try:
        cursor.execute(query=sql, args=sqlargs)
        print('执行sql语句')
        # 提交到数据库执行
        db.commit()
        print('提交数据库')
    except:
        db.rollback()
        print('sql错误')
        flag = False
    cursor.close()
    db.close()
    return flag


def update_pic(uid, dir, tag):
    flag = True
    db = pymysql.connect(host=OPT['host'], user=OPT['user'], passwd=OPT['password'], db=OPT['db'], port=OPT['port'],
                         charset='utf8')
    cursor = db.cursor()
    sql = """UPDATE setupic SET dir=%s,tag=%s WHERE uid=%s"""
    sqlargs = []
    sqlargs.append(dir)
    sqlargs.append(tag)
    sqlargs.append(uid)
    try:
        cursor.execute(query=sql, args=sqlargs)
        print('执行sql语句')
        # 提交到数据库执行
        db.commit()
        print('提交数据库')
    except:
        db.rollback()
        print('sql错误')
        flag = False
    return flag


def find_dir_by_id(uid):
    db = pymysql.connect(host=OPT['host'], user=OPT['user'], passwd=OPT['password'], db=OPT['db'], port=OPT['port'],
                         charset='utf8')
    cursor = db.cursor()
    sql = """SELECT * FROM setupic WHERE uid=%s"""
    sqlargs = []
    dirs = []
    sqlargs.append(uid)
    try:
        cursor.execute(query=sql, args=sqlargs)
        print('执行sql语句')
        results = cursor.fetchall()
        for row in results:
            dirs.append(row[1])
    except:
        print('sql错误')
    cursor.close()
    db.close()
    print(dirs)
    return dirs


def find_ids_by_tag(tag):
    db = pymysql.connect(host=OPT['host'], user=OPT['user'], passwd=OPT['password'], db=OPT['db'], port=OPT['port'],
                         charset='utf8')
    cursor = db.cursor()
    sql = """SELECT * FROM setupic WHERE tag LIKE %s"""
    tag = '%' + tag + '%'
    sqlargs = []
    ids = []
    sqlargs.append(tag)
    try:
        cursor.execute(query=sql, args=sqlargs)
        print('执行sql语句')
        results = cursor.fetchall()
        for row in results:
            ids.append(row[0])
    except:
        print('sql错误')
    cursor.close()
    db.close()
    print(ids)
    return ids
