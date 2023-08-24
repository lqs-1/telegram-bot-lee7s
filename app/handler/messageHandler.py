# Update:从Telegram获取更新
from telegram import Update
# ContextTypes:上下文类型
from telegram.ext import ContextTypes
from app.server.chatServer import get_chat




async def other_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''非命令文字回复 暂时是chatGPT'''
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_chat(update.message.text))