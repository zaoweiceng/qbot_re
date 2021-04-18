from nonebot import on_command, CommandSession
import requests
import time
import csv
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError
import sys
import json

fp = open('./config', encoding='utf8')
fp_text = fp.read()
project_src = json.loads(fp_text)
if project_src['local_project_dir'] != '':
    sys.path.append(project_src['local_project_dir'])
from nonebot.command.argfilter import extractors, validators, controllers
from nonebot import on_command, scheduler
from apscheduler.triggers.date import DateTrigger
import datetime


@on_command('reminder', aliases=('提醒'))
async def reminder(session: CommandSession):
    note = await session.aget(
        'note', prompt='你需要我提醒你什么呢',
        arg_filters=[
            extractors.extract_text,  # 取纯文本部分
            controllers.handle_cancellation(session),  # 处理用户可能的取消指令
            str.strip  # 去掉两边空白字符
        ]
    )

    time = await session.aget(
        'time', prompt='你需要我在什么时间提醒你呢？(格式: 日-小时-分种后)',
        arg_filters=[
            extractors.extract_text,  # 取纯文本部分
            controllers.handle_cancellation(session),  # 处理用户可能的取消指令
            str.strip,  # 去掉两边空白字符
        ]
    )
    time = time.split('-')
    send = await session.aget('send_way', prompt='群提醒: 1\n个人提醒: 2',
                              arg_filters=[
                                  extractors.extract_text,  # 取纯文本部分
                                  controllers.handle_cancellation(session),  # 处理用户可能的取消指令
                                  str.strip,  # 去掉两边空白字符
                              ])
    user_id = session.event['user_id']
    group_id = session.event.group_id
    group_send_id = '1'
    if send == '1':
        group_send_id = await session.aget('group_send_id', prompt='本群提醒: 1\n其它群提醒，群号: ',
                              arg_filters=[
                                  extractors.extract_text,  # 取纯文本部分
                                  controllers.handle_cancellation(session),  # 处理用户可能的取消指令
                                  str.strip,  # 去掉两边空白字符
                              ])
        if group_send_id != '1':
            group_id = group_send_id
    delta = datetime.timedelta(days=int(time[0]), hours=int(time[1]), minutes=int(time[2]))
    trigger = DateTrigger(
        run_date=datetime.datetime.now() + delta
    )
    bot = nonebot.get_bot()
    if group_send_id != '1':
        scheduler.add_job(
            func=bot.send_group_msg,  # 要添加任务的函数，不要带参数
            trigger=trigger,  # 触发器
            #args=(group_id, note,),  # 函数的参数列表，注意：只有一个值时，不能省略末尾的逗号
            kwargs={"group_id":group_id, "message":note},
            misfire_grace_time=60,  # 允许的误差时间，建议不要省略
        )
    else:
        scheduler.add_job(
            func=bot.send_private_msg,  # 要添加任务的函数，不要带参数
            trigger=trigger,  # 触发器
            #args=(user_id, note,),  # 函数的参数列表，注意：只有一个值时，不能省略末尾的逗号
            kwargs={"user_id": user_id, "message": note},
            misfire_grace_time=60,  # 允许的误差时间，建议不要省略
        )
    await session.send('新的提醒已经设置成功！')
