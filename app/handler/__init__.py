# CommandHandler:命令处理器
# MessageHandler:消息处理器
import logging
import os.path

from telegram.ext import CommandHandler, MessageHandler, filters
from telegram.ext._application import Application
from app.handler.commandHandler import start, help, my, get_bot, group, unknown
from app.handler.messageHandler import other_message, file_message


def register_all_handler(application: Application):

    # 添加命令处理器
    logging.info("application register 'start' command handler")
    application.add_handler(CommandHandler('start', start))
    logging.info("application register 'help' command handler")
    application.add_handler(CommandHandler('help', help))
    logging.info("application register 'my' command handler")
    application.add_handler(CommandHandler('my', my))
    logging.info("application register 'group' command handler")
    application.add_handler(CommandHandler('group', group))
    logging.info("application register 'get_bot' command handler")
    application.add_handler(CommandHandler('get_bot', get_bot))

    logging.info("application register not exist command handler")
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    logging.info("application register text handler")
    application.add_handler(MessageHandler(filters.TEXT, other_message))

    logging.info("application register file handler")
    application.add_handler(MessageHandler(filters.AUDIO, file_message))
    application.add_handler(MessageHandler(filters.Document.ALL, file_message))


