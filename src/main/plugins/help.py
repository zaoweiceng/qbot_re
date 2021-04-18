from nonebot import on_command, CommandSession
import sys
import json

fp = open('./config', encoding='utf8')
fp_text = fp.read()
project_src = json.loads(fp_text)
if project_src['local_project_dir'] != '':
    sys.path.append(project_src['local_project_dir'])

from src.main.utils.CQMSG import get_cq_msg


@on_command('command', aliases=('help', '?', '？', '帮助', ''))
async def weather(session: CommandSession):
    fp = open('./readme.txt', encoding='utf8')
    text = fp.read()
    res = []
    res.append(get_cq_msg("text", text))
    res.append(get_cq_msg("image", "./help.jpg"))
    await session.send(res)
