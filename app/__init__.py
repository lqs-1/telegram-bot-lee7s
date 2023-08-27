# ApplicationBuilder:简单立即为构建 bot 对象
import logging
import os

import openai
from telegram.ext import ApplicationBuilder
from app.config import BotConfig
# Application为被创建的bot
from telegram.ext._application import Application
from app.handler import register_all_handler


def create_application() -> Application:
    # 设置日志
    logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s:%(message)s',
                        level=logging.INFO)

    logging.info(f'''
    ♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪
    ♪♪                                                                                                      ♪♪
    ♪♪       ll       eeeeeee   eeeeeee   77777777     sssssss    bb          oooooooo      ttttttttt       ♪♪
    ♪♪       ll       ee   ee   ee   ee         77     ss    s    bb          oo    oo          tt          ♪♪
    ♪♪       ll       eeeeeee   eeeeeee        77        ss       bbbbbbbbb   oo    oo          tt          ♪♪
    ♪♪       ll       ee        ee            77       s    ss    bb     bb   oo    oo          tt          ♪♪
    ♪♪       llllll   eeeeeee   eeeeeee      77        sssssss    bbbbbbbbb   oooooooo          tt          ♪♪
    ♪♪                                                                                                      ♪♪
    ♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪♪
    ''')


    # application = ApplicationBuilder().token(BotConfig.TOKEN).proxy_url(BotConfig.PROXY_URL).get_updates_proxy_url(BotConfig.PROXY_URL).build()
    logging.info("application create start")
    application = ApplicationBuilder().token(BotConfig.TOKEN).build()
    logging.info("application create finish\n")

    # 注册处理器
    logging.info("register handler start")
    register_all_handler(application)
    logging.info("register handler finish\n")

    # 添加openai的key
    logging.info("starter load config start")
    openai.api_key = BotConfig.OPENAI_KEY

    # 创建默认目录
    if not os.path.exists(BotConfig.FILE_UPLOAD_LOCAL_PATH):
        os.makedirs(BotConfig.FILE_UPLOAD_LOCAL_PATH)
    logging.info("starter load config finish\n")

    return application