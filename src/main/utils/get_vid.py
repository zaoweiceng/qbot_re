import sys
import json
import requests
from bs4 import BeautifulSoup

fp = open('./config', encoding='utf8')
fp_text = fp.read()
project_src = json.loads(fp_text)
if project_src['local_project_dir'] != '':
    sys.path.append(project_src['local_project_dir'])


def get_vid(name) -> str:
    fid = name
    url = 'https://api.bilibili.com/x/web-interface/search/type?context=&page=1&keyword=' + name + '&search_type=video'
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'referer': 'https://space.bilibili.com/'
    }
    r = requests.get('https://search.bilibili.com/all?keyword=' + name, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser', from_encoding='utf-8')
    result = soup('div')
    re = str(soup.find_all('a', class_="left-img")[0]).split('/')[5]
    print(re)
    return re
