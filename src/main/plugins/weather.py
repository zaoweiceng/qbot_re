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
import src.main.utils.option as OPT

key = '93d2acd3701747a48ef977ac3629abfb'
url = 'https://devapi.qweather.com/v7/weather/now?location='


def get_weather_info(location: str, city: str) -> str:
    r = requests.get(url + str(location) + '&key=' + key)
    data = r.json()
    timeArray = time.strptime(data['now']['obsTime'].split('+')[0], "%Y-%m-%dT%H:%M")
    Time = str(timeArray.tm_year) + '年' + str(timeArray.tm_mon) + '月' + str(timeArray.tm_mday) + '日 ' + str(
        timeArray.tm_hour) + ':%02d' % (timeArray.tm_min)
    Temp = data['now']['temp']
    Temp = '温度: ' + Temp + '℃'
    BTemp = '体感温度: ' + data['now']['feelsLike'] + '℃'
    city = '城市: ' + city
    Time = '数据更新时间: ' + Time
    res = city + '\n' + '当前天气: ' + data['now']['text'] + '\n' + BTemp + '\n' + Temp + '\n' + Time + '\n'
    return  res


def get_location_info(city):
    f = open('./China-City-List-latest.csv', 'r', encoding='utf8', newline='')
    reader = csv.reader(f)
    location = ''
    rows = [row for row in reader]
    for row in rows:
        if row[2] == city:
            location = row[0]
            print(row[0])
            return location


@on_command('weather', aliases=('天气'))
async def weather(session: CommandSession):
    if session.current_arg_text == '':
        city = session.get('city', prompt='请输入城市名称')
    else:
        city = session.current_arg_text
    location = get_location_info(city)
    res = ''
    if location == '':
        res = '请输入正确的城市名称'
    else:
        res = get_weather_info(location, city)
    await session.send(res)


@nonebot.scheduler.scheduled_job(
    'interval',
    hours=6
    # minutes=1
)
async def _():
    bot = nonebot.get_bot()
    groups = OPT.get_schedule_info()
    for g in groups:
        if g != '':
            try:
                city = OPT.get_group_info()[str(g)]['city']
                location = get_location_info(city)
                res = get_weather_info(location, city)
                try:
                    await bot.send_group_msg(group_id=g,
                                             message=res)
                except CQHttpError:
                    pass
            except:
                pass
