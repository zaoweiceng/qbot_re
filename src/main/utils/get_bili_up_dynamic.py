import requests
from bs4 import BeautifulSoup
import sys
import json

fp = open('./config', encoding='utf8')
fp_text = fp.read()
project_src = json.loads(fp_text)
if project_src['local_project_dir'] != '':
    sys.path.append(project_src['local_project_dir'])
from src.main.utils.CQMSG import get_cq_msg

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
}


def get_dynamic(keyward, num=3):
    if num > 10:
        num = 10
    res_lst = []
    r = requests.get(
        'https://api.bilibili.com/x/web-interface/search/type?context=&search_type=bili_user&page=1&keyword=' + keyward,
        headers=header)
    id = json.loads(r.text)['data']['result'][0]['mid']
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=' + str(
        id) + '&offset_dynamic_id='
    res = requests.get(url, header)
    data = res.json()
    cards = data['data']['cards']
    i = 1
    for card in cards:
        d = json.loads(card['card'])
        lst = []
        flag = 0
        try:
            try:
                lst.append(get_cq_msg("text", '第' + str(i) + '条动态:'))
                lst.append(get_cq_msg("text", d['item']['content']))
                try:
                    lst.append(get_cq_msg("text", '\n 转发:\n'))
                    try:
                        lst.append(get_cq_msg("text", json.loads(d['origin'])['item']['description']))
                        lst.append(get_cq_msg("image", json.loads(d['origin'])['item']['pictures'][0]['img_src']))
                    except:
                        lst.append(get_cq_msg("text", json.loads(d['origin'])['title']))
                        av_url = '\n https://www.bilibili.com/video/' + json.loads(d['origin'])['jump_url'].split('/')[
                            3]
                        lst.append(get_cq_msg("text", av_url))
                        lst.append(get_cq_msg("image", json.loads(d['origin'])['pic']))
                except:
                    pass
                flag = 1
                i += 1
            except Exception:
                lst.clear()
                lst.append(get_cq_msg("text", '第' + str(i) + '条动态:'))
                lst.append(get_cq_msg("text", d['desc']))
                av_url = '\n https://www.bilibili.com/video/' + d['jump_url'].split('/')[3]
                lst.append(get_cq_msg("text", av_url))
                lst.append(get_cq_msg("image", d['pic']))
                flag = 1
                i += 1
        except Exception:
            lst.clear()
            lst.append(get_cq_msg("text", '第' + str(i) + '条动态:'))
            lst.append(get_cq_msg("text", d['item']['description']))
            flag = 1
            i += 1
            try:
                for img in d['item']['pictures']:
                    lst.append(get_cq_msg("image", img['img_src']))
            except: pass
        if flag != 0:
            for ii in lst:
                res_lst.append(ii)
                res_lst.append(get_cq_msg("text", '\n \n'))
        if i > num:
            return res_lst
    return res_lst


if __name__ == '__main__':
    lst = get_dynamic('原神', num=2)
    print(lst)
