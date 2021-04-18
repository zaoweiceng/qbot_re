import requests
from PIL import Image
import sys
import random
import json
import src.main.utils.option as option
from io import BytesIO
import os
import src.main.pysql.pysql_setu as pysql

fp = open('./config', encoding='utf8')
fp_text = fp.read()
project_src = json.loads(fp_text)
if project_src['local_project_dir'] != '':
    sys.path.append(project_src['local_project_dir'])


def get_pic(r18=0, keyword='') -> tuple:
    opt = option.get_option()
    url = opt['web_url'] + '?r18=' + str(r18) + '&size1200=true' + '&apikey=' + opt['apikey'] + '&keyword=' + keyword
    response = requests.get(url)
    data = response.json()
    quota = data['quota']
    code = data['code']
    if code == 429:
        return 429, '', quota
    elif code == -1:
        return -1, '', quota
    elif code == 401:
        return 401, '', quota
    elif code == 404:
        return 404, '', quota
    elif code == 403:
        return 403, '', quota
    pic_url = data['data'][0]['url']
    img_name = pic_url.split('/')[-1]
    loc = opt['cache_dir'] + img_name
    if not os.path.exists(loc):
        print("本地无图片，开始下载")
        img = requests.get(pic_url)
        img_cache = Image.open(BytesIO(img.content))
        img_cache.save(loc, quality=80)
        print("下载完成")
    return 0, loc, quota


def get_pic_from_sql(tag: str) -> str:
    lst = pysql.find_ids_by_tag(tag)
    n = random.randint(0, lst.__len__() - 1)
    src = get_local_dir(lst[n], option.get_option()['sql_dir'])
    src = src + os.listdir(src)[0]
    print(src)
    return src


def get_local_dir(id: str, local_dir: str) -> str:
    d = ''
    for j in id:
        d = d + j + '/'
        if not os.path.exists(local_dir + d):
            os.mkdir(local_dir + d)
    return local_dir + d


def get_pic_from_local() -> str:
    opt = option.get_option()
    location = random.randint(0, opt['local_pic_num'])
    url = opt['local_dir'] + str(location) + '.png'
    return url
