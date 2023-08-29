# Update:从Telegram获取更新
import json
import logging
import os

import requests
from sqlalchemy import and_
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# ContextTypes:上下文类型
from telegram.ext import ContextTypes

from app import BotConfig
from app.db.models import UserFile, User
from app.server import chatServer
from app.server.fileServer import no_keyword, has_keyword, construct_file
from app.utils.filePaginationUtils import reply_markup_generator

PAGE_SIZE = 1


# start命令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''响应start命令'''

    text = '您好 我是一个智能机器人'
    logging.info(f"用户 {update.message.chat.username} 开始使用机器人了")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


# help命令
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''响应help命令'''

    text = '直接输入文本可以当作chatGPT用\n' \
           '机器人对接的gpt3.5\n\n' \
           '用户发送文件可以直接保存文件\n' \
           '(20MB以内,一个一个上传) \n' \
           '并在上传到云之后返回文件公网链接\n\n' \
           '/start 开始使用机器人\n' \
           '/help 获取使用帮助\n' \
           '/my 获取个人信息,仅个人机器人页面使用\n' \
           '/group 获取群组信息,仅群组使用\n' \
           '/get_bot 获取机器人,仅开发者使用\n' \
           '/get_file 获取文件 无参查所有 有参模糊查\n' \
           '/get_f_list 获取文件 分页模式 用法同上'

    logging.info(f"用户 {update.message.chat.username} 获取了帮助信息")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


# my命令
async def my(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''返回用户个人信息'''

    # 如果是个人账号就返回个人信息 如果不是个人账号就返回错误提示
    if update.message.chat.type.title() == 'Private':
        # 用户id
        u_id = update.message.chat.id
        # 昵称
        nic_name = update.message.chat.first_name
        # 账号
        account = update.message.chat.username
        result = f'uid: {u_id}\n昵称: {nic_name}\n账号: @{account}'

        logging.info(f"用户 {update.message.chat.username} 获取了个人信息 {u_id} {nic_name} {account}")

        await context.bot.send_message(chat_id=u_id, text=result)

    else:
        logging.info(f"用户 {update.message.chat.username} 获取了个人信息 但是走错地方了")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="此命令只可在机器人页面个人使用")


# group命令
async def group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''获取群组信息'''

    # 如果是个人账号就返回错误信息 如果是群组就返回群组信息
    if update.message.chat.type.title() == 'Supergroup':
        # 群组id
        g_id = update.message.chat.id
        # 群组名称
        g_name = update.message.chat.title
        # 群组账号
        g_account = f'https://t.me/{update.message.chat.username}'
        result = f'g_id: {g_id}\n群组名: {g_name}\n群组账号: {g_account}'

        logging.info(f"用户 {update.message.from_user.username} 获取了群组信息 {g_id} {g_name} {g_account}")

        await context.bot.send_message(chat_id=g_id, text=result)

    else:
        logging.info(f"用户 {update.message.chat.username} 获取了群组信息 但是走错地方了")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="此命令只可在群组页面使用")


# get_bot命令
async def get_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''获取机器人信息'''

    # 如果是开发者就返回机器人信息 如果是其他就返回错误信息
    if update.message.chat.id == 5060527090:
        bot_id = context.bot.id
        bot_name = context.bot.username
        bot_account = context.bot.name
        result = f'bot_id: {bot_id}\nbot_name: {bot_name}\nbot_account: {bot_account}'

        logging.info(f"开发人员 {update.message.chat.username} 获取了机器人信息 {bot_id} {bot_name} {bot_account}")

        await context.bot.send_message(chat_id=update.message.chat.id, text=result)

    else:
        logging.info(f"用户 {update.message.chat.username} 妄图获取机器人信息")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="此命令只可由开发者机器人页面使用使用")


# 当命令不存在的时候
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''响应未知命令'''

    text = "此命令有待开发~\n有问题请联系: @lee7s_tg"

    logging.info(f"用户 {update.message.chat.username} 使用了未开发命令")

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''获取个人文件 直接返回'''
    await context.bot.send_message(chat_id=update.effective_chat.id, text="请等待...")
    file_list = await construct_file(update, context)
    await context.bot.delete_message(update.effective_chat.id, update.effective_message.id + 1)
    for file in file_list:
        try:
            await context.bot.send_document(chat_id=update.effective_chat.id,
                                            document=os.path.join(BotConfig.WEB_FILE_PREFIX, file.file))
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"{file.fileName}\n" + os.path.join(BotConfig.WEB_FILE_PREFIX,
                                                                                    file.file))






async def get_file_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''获取个人文件 分页列表'''

    await context.bot.send_message(chat_id=update.effective_chat.id, text="请等待...")
    file_list = await construct_file(update, context)
    total_file_num = len(file_list)
    await context.bot.delete_message(update.effective_chat.id, update.effective_message.id + 1)
    context.user_data["user_text"] = update.message.text
    # 构造数据
    file_list, keyboard = reply_markup_generator(file_list, 1, BotConfig.PER_PAGE_FILE_SIZE)
    result_list = list()
    number = 1
    for file in file_list:
        result_list.append(
            f"{number} -- <a href='{os.path.join(BotConfig.WEB_FILE_PREFIX, file.file)}'>{file.fileName}</a>")

        number += 1

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="\n\n".join(result_list) + f"\n\n第{1}页 共{total_file_num}文件",
                                   parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard),
                                   disable_web_page_preview=True)


async def reply_file_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """点击页码可以分页展示文件"""

    query = update.callback_query
    from app import session
    chat_id = update.effective_chat.id
    await query.answer()

    # 查出对应的用户 如果没有就是没有上传过文件
    tg_user = session.query(User).filter(User.username == str(chat_id)).first()

    if tg_user is None:
        return await context.bot.send_message(chat_id=chat_id, text="您还未上传过文件")

    # 是否为模糊匹配
    try:
        if len(context.user_data.get("user_text").split(" ")) >= 2:
            file_name = context.user_data.get("user_text").split(" ")[-1]
            file_list = has_keyword(session, file_name, tg_user.id, chat_id)
            total_file_num = len(file_list)
            file_list, keyboard = reply_markup_generator(file_list, int(query.data), BotConfig.PER_PAGE_FILE_SIZE)
            result_list = list()
            number = 1
            for file in file_list:
                result_list.append(
                    f"{number} -- <a href='{os.path.join(BotConfig.WEB_FILE_PREFIX, file.file)}'>{file.fileName}</a>")
                number += 1

            return await query.edit_message_text(
                text="\n\n".join(result_list) + f"\n\n第{query.data}页 共{total_file_num}文件", parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

    except Exception as e:
        return

    # except Exception as e:
    try:
        file_list = no_keyword(session, tg_user.id, chat_id)
        total_file_num = len(file_list)
        file_list, keyboard = reply_markup_generator(file_list, int(query.data), BotConfig.PER_PAGE_FILE_SIZE)
        result_list = list()
        number = 1
        for file in file_list:
            result_list.append(
                f"{number} -- <a href='{os.path.join(BotConfig.WEB_FILE_PREFIX, file.file)}'>{file.fileName}</a>")

            number += 1

        await query.edit_message_text(text="\n\n".join(result_list) + f"\n\n第{query.data}页 共{total_file_num}文件",
                                      parse_mode='HTML',
                                      reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

    except Exception as e:
        return





async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """定时任务回调函数"""
    job = context.job
    # response = requests.get(BotConfig.WEIBO_NEWS_REQUEST_API, headers={"username": "5060527090"})
    # data_list = response.json().get('result_list')
    # result_list = list()
    # for index in range():
    await context.bot.send_message("-1001679451720", text=chatServer.get_chat("给我发一句励志语录"))


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """删除定时任务"""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """添加一个定时任务"""
    chat_id = update.effective_chat.id
    try:
        # 获取定时间隔时间
        timer = float(context.args[0])
        if timer < 0:
            await update.effective_message.reply_text("定时时间不能小于0")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(alarm, interval=timer, first=1, name=str(chat_id))

        text = "定时任务设置成功"
        if job_removed:
            text += " 且删除了旧任务"
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("设置失败 请重新设置")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """取消定时任务."""
    chat_id = update.effective_chat.id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "任务取消成功" if job_removed else "你没有任务可以取消"
    await update.message.reply_text(text)