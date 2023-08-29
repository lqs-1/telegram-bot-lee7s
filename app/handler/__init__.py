# CommandHandler:命令处理器
# MessageHandler:消息处理器
import logging

from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.ext._application import Application
from app.handler.commandHandler import start, help, my, get_bot, group, unknown, get_file, reply_file_page, \
    get_file_list, set_timer, unset
from app.handler.messageHandler import other_message, file_message


def register_all_handler(application: Application):
    # 添加命令处理器
    logging.info("application register 'start' command handler")
    application.add_handler(CommandHandler('start', start, block=False))
    logging.info("application register 'help' command handler")
    application.add_handler(CommandHandler('help', help, block=False))
    logging.info("application register 'my' command handler")
    application.add_handler(CommandHandler('my', my, block=False))
    logging.info("application register 'group' command handler")
    application.add_handler(CommandHandler('group', group, block=False))
    logging.info("application register 'get_bot' command handler")
    application.add_handler(CommandHandler('get_bot', get_bot, block=False))
    logging.info("application register 'get_file' command handler")
    application.add_handler(CommandHandler('get_file', get_file, block=False))
    application.add_handler(CommandHandler('get_f_list', get_file_list, block=False))
    application.add_handler(CommandHandler("set", set_timer))
    application.add_handler(CommandHandler("unset", unset))

    logging.info("application register not exist command handler")
    application.add_handler(MessageHandler(filters.COMMAND, unknown, block=False))
    logging.info("application register text handler")
    application.add_handler(MessageHandler(filters.TEXT, other_message, block=False))

    logging.info("application register file handler")
    application.add_handler(MessageHandler(filters.AUDIO, file_message, block=False))
    application.add_handler(MessageHandler(filters.Document.ALL, file_message))

    logging.info("application register query handler")
    application.add_handler(CallbackQueryHandler(reply_file_page, block=False))
