import json


def get_option():
    fp = open('./config', encoding='utf8')
    text = fp.read()
    return json.loads(text)


def get_sql_info():
    fp = open('./sqlInfo', encoding='utf8')
    text = fp.read()
    return json.loads(text)


def get_schedule_info():
    fp = open('./schedule', encoding='utf8')
    lst = []
    for ii in fp:
        s = ii[:-1]
        lst.append(s)
    return lst


def get_group_info():
    fp = open('./group_id', encoding='utf8')
    text = fp.read()
    return json.loads(text)


OPT = get_option()