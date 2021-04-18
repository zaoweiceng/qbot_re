# -*- coding: utf-8 -*-
import nonebot
import sys
# Linux环境下填写项目根路径
# sys.path.append('/usr/local/qbot/bot/')
import src.main.config as config
import os

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__), 'plugins'),
        'plugins'
    )

    nonebot.run()