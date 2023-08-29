import os
from operator import and_

from sqlalchemy import Update
from telegram.ext import ContextTypes

from app.db.models import UserFile, User



async def construct_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """获取文件方法抽取"""
    from app import session, BotConfig

    chat_id = update.message.chat.id

    # 查出对应的用户 如果没有就是没有上传过文件
    tg_user = session.query(User).filter(User.username == str(chat_id)).first()

    if tg_user is None:
        return await context.bot.send_message(chat_id=chat_id, text="您还未上传过文件")

    # 是否为模糊匹配
    if len(update.message.text.split(" ")) >= 2:
        file_name = update.message.text.split(" ")[-1]
        file_list = has_keyword(session, file_name, tg_user.id, chat_id)

    # 全查
    else:
        file_list = no_keyword(session, tg_user.id, chat_id)

    return file_list

def has_keyword(session, keyword, tg_user_id, chat_id):
    """
    关键字查询
    :param session:
    :param keyword:
    :param tg_user_id:
    :param chat_id:
    :return:
    """
    file_list = session.query(UserFile).filter(
        and_(UserFile.userId == tg_user_id, UserFile.fileName.like(f"%{keyword}%"))).order_by(UserFile.uploadTime.desc()).all()
    if chat_id == 5060527090:
        lee7s_file_list = session.query(UserFile).filter(
            and_(UserFile.userId == 46, UserFile.fileName.like(f"%{keyword}%"))).order_by(UserFile.uploadTime.desc()).all()
        file_list = file_list + lee7s_file_list
    session.close()
    return file_list


def no_keyword(session, tg_user_id, chat_id):
    """非关键字查询"""
    file_list = session.query(UserFile).filter(UserFile.userId == tg_user_id).order_by(UserFile.uploadTime.desc()).all()
    if chat_id == 5060527090:
        lee7s_file_list = session.query(UserFile).filter(UserFile.userId == 46).order_by(UserFile.uploadTime.desc()).all()
        file_list = file_list + lee7s_file_list
    session.close()
    return file_list



def get_file_by_part_url(file_url_part : str, g_user_id : str) -> str:
    """
    根据部分文件链接获取完整url
    :param file_file:
    :return:
    """

    from app import session, BotConfig

    user_file = session.query(UserFile).filter(UserFile.file.like(f'%{file_url_part}%')).first()

    return os.path.join(BotConfig.WEB_FILE_PREFIX, user_file.file) if user_file is not None else ""