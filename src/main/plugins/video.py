from nonebot import on_command, CommandSession
import sys
import json
fp = open('./config', encoding='utf8')
fp_text = fp.read()
project_src = json.loads(fp_text)
if project_src['local_project_dir'] != '':
    sys.path.append(project_src['local_project_dir'])
from src.main.utils.get_vid import get_vid


@on_command('fan', aliases=('动漫', '番剧', '电影'))
async def fan(session: CommandSession):
    print('执行fan')
    if session.current_arg_text == '':
        res = '请先输入你要查找的番剧！'
    else:
        try:
            fid = get_vid(session.current_arg_text)
            res = '《'+session.current_arg_text+'》的链接为：https://m.bilibili.com/bangumi/play/'+fid+'\n开始观看吧！'
        except Exception:
            res = '未找到该动漫，请检查名字是否正确（或B站没有该资源），这边给您推荐:\nhttps://www.bilibili.com/bangumi/play/ss33343'
    await session.send(res)


