from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession
import sys
import json

fp = open('./config', encoding='utf8')
fp_text = fp.read()
project_src = json.loads(fp_text)
sys.path.append(project_src['local_project_dir'])
import src.main.utils.option as option
from src.main.utils.CQMSG import get_cq_msg
from src.main.utils.get_pic import get_pic, get_pic_from_local, get_pic_from_sql
from src.main.utils.get_random_pic import get_random_src


def isnumber(s):
    try:
        int(s)
        return True
    except Exception:
        pass


@on_command('setu_local', aliases=('图', 't'))
async def setu(session: CommandSession):
    print('执行setu' + session.current_arg_text)
    res = []
    code = 0
    if session.current_arg_text == '':
        src = get_random_src(option.get_option()['sql_dir'])
        res.append(get_cq_msg("text", "恭喜你获得老婆一只！"))
        res.append(get_cq_msg("image", src))
    else:
        s = session.current_arg_text
        if isnumber(s):
            num = int(session.current_arg_text)
            if num >= 10:
                await session.send('做人不能太贪心哦！', at_sender=True)
                num = 1
            for i in range(num):
                src = get_random_src(option.get_option()['sql_dir'])
                res.append(get_cq_msg("image", src))
            res.append(get_cq_msg("text", '共计获得老婆' + str(num) + '只！'))
        else:
            try:
                src = get_pic_from_sql(session.current_arg_text)
                res.append(get_cq_msg("text", '恭喜你获得' + session.current_arg_text.strip() + '老婆一只！'))
            except Exception:
                src = get_random_src(option.get_option()['sql_dir'])
                res.append(get_cq_msg("text", '网络受到神秘的非物质力量干扰，故老婆丢失，这边给您换了一个'))
    await session.send(res, at_sender=True)
