from nonebot import on_command, CommandSession
import requests
import time
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
import sys
import json
import os

fp = open('./config', encoding='utf8')
fp_text = fp.read()
project_src = json.loads(fp_text)
if project_src['local_project_dir'] != '':
    sys.path.append(project_src['local_project_dir'])
from src.main.utils.get_bili_up_dynamic import get_dynamic
import src.main.utils.option as OPT


def isnumber(s):
    try:
        int(s)
        return True
    except Exception:
        return False


def rm_cache():
    path = json.loads(fp_text)['mcl_dir']
    dirs = os.listdir(path)
    for f in dirs:
        os.remove(path + f)


@on_command('dynamic', aliases=('动态'))
async def dynamic(session: CommandSession):
    rm_cache()
    s = session.current_arg_text
    up_name = s
    lst = s.split(' ')
    if lst.__len__() > 1:
        up_name = lst[0]
        dynammic_num = lst[1]
        if isnumber(dynammic_num):
            # print('-----' + up_name + '-------', dynammic_num)
            res = get_dynamic(up_name, num=int(dynammic_num))
            print(res)
            await session.send(res)
    else:
        await session.send(get_dynamic(up_name))


@nonebot.scheduler.scheduled_job('cron', hour=8)
async def morning():
    bot = nonebot.get_bot()
    groups = OPT.get_schedule_info()
    for g in groups:
        if g != '':
            try:
                up_name = OPT.get_group_info()[str(g)]['dynamic']
                try:
                    rm_cache()
                    await bot.send_group_msg(group_id=g, message=get_dynamic('央视新闻', num=5))
                except CQHttpError:
                    pass
            except:
                pass


@nonebot.scheduler.scheduled_job('cron', hour=19)
async def night():
    bot = nonebot.get_bot()
    groups = OPT.get_schedule_info()
    for g in groups:
        if g != '':
            try:
                up_name = OPT.get_group_info()[str(g)]['dynamic']
                try:
                    rm_cache()
                    await bot.send_group_msg(group_id=g, message=get_dynamic('央视新闻', num=5))
                except CQHttpError:
                    pass
            except:
                pass
