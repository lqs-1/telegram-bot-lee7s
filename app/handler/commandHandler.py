# Update:从Telegram获取更新
import logging

from sqlalchemy import and_
from telegram import Update
# ContextTypes:上下文类型
from telegram.ext import ContextTypes

from app import BotConfig
from app.db.models import UserFile, User


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
           '/get_bot 获取机器人信息,仅开发者机器人页面使用\n' \
           '/get_file 获取个人文件 直接用获取全部 /get_file 文件名 可模糊查询'

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
    '''获取个人文件'''
    from app import session

    # 查出对应的用户 如果没有就是没有上传过文件
    tg_user = session.query(User).filter(User.username == str(update.message.chat.id)).first()

    if tg_user is None:
        return await context.bot.send_message(chat_id=update.message.chat.id, text="您还未上传过文件")

    # 是否为模糊匹配
    if len(update.message.text.split(" ")) >= 2:
        file_name = update.message.text.split(" ")[-1]
        file_list = session.query(UserFile).filter(and_(UserFile.userId == tg_user.id, UserFile.fileName.like(f"%{file_name}%"))).all()
        for file in file_list:
            await context.bot.send_message(chat_id=update.message.chat.id,text=f'{file.fileName}: {BotConfig.WEB_FILE_PREFIX + file.file}')
    # 全查
    else:

        file_list = session.query(UserFile).filter(UserFile.userId == tg_user.id).all()

        for file in file_list:
            await context.bot.send_message(chat_id=update.message.chat.id, text=f'{file.fileName}: {BotConfig.WEB_FILE_PREFIX + file.file}')










