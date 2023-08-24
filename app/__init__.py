# ApplicationBuilder:简单立即为构建 bot 对象
import openai
from telegram.ext import ApplicationBuilder
from app.config import BotConfig
# Application为被创建的bot
from telegram.ext._application import Application
from app.handler import register_all_handler


def create_application() -> Application:
    # application = ApplicationBuilder().token(BotConfig.TOKEN).proxy_url(BotConfig.PROXY_URL).get_updates_proxy_url(BotConfig.PROXY_URL).build()
    application = ApplicationBuilder().token(BotConfig.TOKEN).build()

    # 注册处理器
    register_all_handler(application)

    # 添加openai的key
    openai.api_key = BotConfig.OPENAI_KEY

    return application