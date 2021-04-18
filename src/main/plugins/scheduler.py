import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
#
# @nonebot.scheduler.scheduled_job(
#     'cron',
#     # year=None,
#     # month=None,
#     # day=None,
#     # week=None,
#     day_of_week="mon,tue,wed,thu,fri",
#     hour=23,
#     minute='*',
#     # second=20,
#     # start_date=None,
#     # end_date=None,
#     # timezone=None,
# )
# async def _():
#     bot = nonebot.get_bot()
#     try:
#         await bot.send_group_msg(group_id=1094685133,
#                                  message=f'!!!')
#     except CQHttpError:
#         pass