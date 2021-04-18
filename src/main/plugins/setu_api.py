from aiocqhttp import MessageSegment
from nonebot import on_command, CommandSession
import sys
import json

fp = open('./config', encoding='utf8')
fp_text = fp.read()
project_src = json.loads(fp_text)
if project_src['local_project_dir'] != '':
    sys.path.append(project_src['local_project_dir'])
from src.main.utils.get_pic import get_pic, get_pic_from_local
from src.main.utils.CQMSG import get_cq_msg


def isnumber(s):
    try:
        int(s)
        return True
    except Exception:
        pass


@on_command('setu', aliases=('涩图', '色图', '来一张涩图', '来一张色图', '来点涩图', '来点色图'))
async def setu(session: CommandSession):
    print('执行setu' + session.current_arg_text)
    res = []
    code = 0
    if session.current_arg_text == '':
        src = get_pic_from_local()
        res.append(get_cq_msg("text", "恭喜你获得老婆一只！"))
        res.append(get_cq_msg("image", src))
    else:
        s = session.current_arg_text
        if isnumber(s):
            num = int(session.current_arg_text)
            if num >= 10:
                res.append(get_cq_msg("text", "做人不能太贪心哦！"))
                num = 1
            for i in range(num):
                src = get_pic_from_local()
                res.append(get_cq_msg("image", src))
            res.append(get_cq_msg("text", '共计获得老婆' + str(num) + '只！'))
        else:
            try:
                code, src, quota = get_pic(r18=0, keyword=session.current_arg_text)
                if code == 0:
                    res.append(get_cq_msg("text", '恭喜你获得' + session.current_arg_text.strip() + '老婆一只！'))
                else:
                    src = get_pic_from_local()
                    if code == -1:
                        print('api内部错误')
                    elif code == 401:
                        print('由于不规范的操作而被拒绝调用')
                    elif code == 403:
                        print('找不到符合关键字的色图')
                    elif code == 429:
                        print('达到调用额度限制')
                res.append(get_cq_msg("image", src))
                await session.send(ensure_private=json.loads(fp_text)['QQ'], message='剩余服务次数：' + str(quota))

            except Exception:
                src = get_pic_from_local()
                res.append(get_cq_msg("text", '网络受到神秘的非物质力量干扰，故老婆丢失，这边给您换了一个'))
    await session.send(res, at_sender=True)
