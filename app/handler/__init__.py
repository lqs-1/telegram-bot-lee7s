# CommandHandler:命令处理器
# MessageHandler:消息处理器
from telegram.ext import CommandHandler, MessageHandler, filters
from telegram.ext._application import Application
from app.handler.commandHandler import start, help, my, get_bot, group, unknown
from app.handler.messageHandler import other_message


def register_all_handler(application: Application):
    # 添加命令处理器
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('my', my))
    application.add_handler(CommandHandler('group', group))
    application.add_handler(CommandHandler('get_bot', get_bot))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_handler(MessageHandler(filters.TEXT, other_message))
