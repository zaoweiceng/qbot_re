from nonebot import on_command, CommandSession
import sys
import json

from nonebot.command.argfilter import extractors, controllers
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

fp = open('./config', encoding='utf8')
fp_text = fp.read()
project_src = json.loads(fp_text)
if project_src['local_project_dir'] != '':
    sys.path.append(project_src['local_project_dir'])
import src.main.pysql.school as ps

url = 'http://login.cuit.edu.cn/Login/xLogin/Login.asp'
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/usr/bin/chromedriver')


@on_command('school', aliases='打卡')
async def school(session: CommandSession):
    args = session.current_arg_text.strip()
    if args == '':
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/usr/bin/chromedriver')
        driver.get(url)
        time.sleep(3)
        data = json.loads(fp_text)
        input_username = ''
        input_password = ''
        try:
            flag, usernames, passwords = ps.find_nopassword_by_qqno(session.event['user_id'])
            if flag is False:
                id = await session.aget(
                    'id', prompt='暂无信息，是否需要录入信息：\n'
                                 '录入回复1，结束回复0',
                    arg_filters=[
                        extractors.extract_text,  # 取纯文本部分
                        controllers.handle_cancellation(session),  # 处理用户可能的取消指令
                        str.strip  # 去掉两边空白字符
                    ]
                )
                if id == '1':
                    await add_user_indo(session)
                    return
                else:
                    return
            input_username = usernames
            input_password = passwords
        except:
            return
        username = driver.find_element_by_id('txtId')
        password = driver.find_element_by_id('txtMM')
        submit = driver.find_element_by_id('IbtnEnter')
        username.send_keys(input_username)
        password.send_keys(input_password)
        submit.click()
        time.sleep(3)
        try:
            new_day = driver.find_element_by_xpath('/html/body/div[2]/table/tbody[2]/tr[2]/td[2]/a')
            new_day.click()
            time.sleep(3)
            input_target_place = '校外(=・ω・=)'
            input_target_thing = '出校✿ヽ(°▽°)ノ✿'
            target_place = driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[5]/td[2]/div/input[1]')
            target_thing = driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[5]/td[2]/div/input[2]')
            plan_out = driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[5]/td[2]/div/select[1]')
            plan_out_time = driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[5]/td[2]/div/select[2]')
            plan_in = driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[5]/td[2]/div/select[3]')
            plan_in_time = driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[5]/td[2]/div/select[4]')
            target_place.send_keys(input_target_place)
            target_thing.send_keys(input_target_thing)
            Select(plan_out).select_by_value("1")
            Select(plan_in).select_by_value("1")
            Select(plan_out_time).select_by_value("06")
            Select(plan_in_time).select_by_value("23")
            Select(driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[4]/td[2]/div/select[1]')).select_by_value("1")
            Select(driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[4]/td[2]/div/select[2]')).select_by_value("1")
            Select(driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[4]/td[2]/div/select[3]')).select_by_value("1")
            Select(driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[4]/td[2]/div/select[4]')).select_by_value("1")
            Select(driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[4]/td[2]/div/select[5]')).select_by_value("1")
            Select(driver.find_element_by_xpath('//*[@id="wjTA"]/tbody/tr[4]/td[2]/div/select[6]')).select_by_value("1")
            driver.find_element_by_xpath('/html/body/form/div[1]/table/tbody/tr/td[1]/input').click()
        except Exception:
            await session.send('打卡失败')
        driver.quit()
        await session.send('打卡成功')
    elif args == '?' or args == '？' or args == 'help' or args == '帮助':
        await session.send('功能如下:\n'
                           '1、申请出校: 打卡\n'
                           '2、修改账号和密码: 修改密码，之后按照提示操作\n'
                           '3、第一次使用: 录入信息\n'
                           '4、删除信息: 删除')
    elif args == '修改密码':
        try:
            await change_password(session)
        except:
            await session.send('修改失败')
    elif args == '录入信息':
        try:
            await add_user_indo(session)
        except:
            await session.send('录入失败，请重试')
    elif args == '删除':
        await del_user_info(session)


async def add_user_indo(session: CommandSession):
    lst = await get_username_and_password(session)
    qq = lst[0]
    username = lst[1]
    password = lst[2]
    ps.insert_all(username, password, qq)
    await session.send('添加成功')


async def del_user_info(session: CommandSession):
    ps.delete_by_qqno(session.event['user_id'])
    await session.send('删除成功')


async def change_password(session: CommandSession):
    lst = await get_username_and_password(session)
    qq = lst[0]
    username = lst[1]
    password = lst[2]
    ps.update_nopassword_by_qqno(username, password, qq)
    await session.send('修改成功')


async def get_username_and_password(session: CommandSession):
    qq = session.event['user_id']
    username = await session.aget(
        'username', prompt='请输入账号：',
        arg_filters=[
            extractors.extract_text,  # 取纯文本部分
            controllers.handle_cancellation(session),  # 处理用户可能的取消指令
            str.strip  # 去掉两边空白字符
        ]
    )
    password = await session.aget(
        'password', prompt='请输入密码：',
        arg_filters=[
            extractors.extract_text,  # 取纯文本部分
            controllers.handle_cancellation(session),  # 处理用户可能的取消指令
            str.strip  # 去掉两边空白字符
        ]
    )
    print(qq, username, password)
    return [qq, username, password]
