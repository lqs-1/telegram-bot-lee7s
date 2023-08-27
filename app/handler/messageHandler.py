# Update:从Telegram获取更新
import logging
import uuid

from telegram import Update
# ContextTypes:上下文类型
from telegram.ext import ContextTypes
import requests
import json
import os

from app import BotConfig
from app.db import User
from app.db.models import UserFile, UserRole, UserPermission, UserMenu
from app.server.chatServer import get_chat


async def other_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''非命令文字回复 暂时是chatGPT'''

    logging.info(f"用户 {update.message.chat.username} 提问 {update.message.text}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_chat(update.message.text))


async def file_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''非命令文件回复 上传到aliyun

    '''

    from app import session

    chat_id = update.effective_chat.id
    message_id = update.effective_message.id

    # 查出对应的用户 如果没有就创建出来 如果有的话 直接保存文件
    tg_user = session.query(User).filter(User.username == str(chat_id)).first()
    if tg_user is None:
        # 创建用户
        tg_user = User(username=str(chat_id), password=BotConfig.TG_USER_LOGIN_MANAGER_PASSWORD, sex="男", email=f"{uuid.uuid4().hex}@gmail.com")
        session.add(tg_user)
        session.commit()

        # 添加角色
        tg_user_role = UserRole(userId=tg_user.id, roleId=1)
        session.add(tg_user_role)

        # 添加权限
        tg_user_permission = UserPermission(userId=tg_user.id, permissionId=1)
        session.add(tg_user_permission)

        # 添加菜单
        tg_user_menu_1 = UserMenu(userId=tg_user.id, menuId=1)
        tg_user_menu_2 = UserMenu(userId=tg_user.id, menuId=6)
        tg_user_menu_3 = UserMenu(userId=tg_user.id, menuId=47)
        session.add(tg_user_menu_1)
        session.add(tg_user_menu_2)
        session.add(tg_user_menu_3)

        session.commit()



    # 解析各种数据
    file_id = update.message.audio.file_id if update.message.document is None else update.message.document.file_id
    file_name = update.message.audio.file_name if update.message.document is None else update.message.document.file_name
    file_size = update.message.audio.file_size if update.message.document is None else update.message.document.file_size

    if file_size > 20*1024*1024:
        logging.info(f"用户 {update.message.chat.username} 上传文件太大了 {file_size} 字节")
        return await context.bot.send_message(chat_id=update.effective_chat.id, text="尊敬的用户请上传20MB以内的文件!!!")

    file_unique_id = update.message.audio.file_unique_id if update.message.document is None else update.message.document.file_unique_id

    # 获取文件
    file = await context.bot.get_file(file_id)

    # 将文件存储到本地
    await context.bot.send_message(chat_id=update.effective_chat.id, text="请等待,正在上传...")

    # 删除自己刚刚发的消息
    # await context.bot.delete_message(chat_id, message_id)

    # 将文件保存到本地
    await file.download_to_drive(os.path.join(BotConfig.FILE_UPLOAD_LOCAL_PATH, file_name), )

    # 上传文件到云上
    response = requests.post(BotConfig.FILE_UPLOAD_SYSTEM_PATH, files={"file": open(os.path.join(BotConfig.FILE_UPLOAD_LOCAL_PATH, file_name), "rb")})
    # 将数据解析成json
    result = json.loads(response.text)

    # 删除本地文件
    os.remove(os.path.join(BotConfig.FILE_UPLOAD_LOCAL_PATH, file_name))

    # 删除机器人刚刚发的消息
    await context.bot.delete_message(chat_id, message_id + 1)

    logging.info(f"用户 {update.message.chat.username} 上传文件 {file_name} {file_size} 字节")

    # 将上传到云的数据报错到数据库
    tg_file = UserFile(userId=tg_user.id, file=str(result.get("web-file-url")).split(BotConfig.WEB_FILE_PREFIX)[1], fileType="tg_file", fileName=file_name)
    session.add(tg_file)
    session.commit()


    await context.bot.send_message(chat_id=update.effective_chat.id, text=result.get("msg") + "\n" + result.get("web-file-url"))
