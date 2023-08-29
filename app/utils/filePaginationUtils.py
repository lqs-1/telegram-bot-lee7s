from telegram import InlineKeyboardButton

from app import BotConfig


def reply_markup_generator(origin_data_list, to_page, page_limit):
    """键盘和分页数据生成器"""
    # 键盘
    keyboard = list()
    # 算出要分多少页数
    total_page = (len(origin_data_list) + page_limit - 1) // page_limit
    # 计算分页布局 每行5个页码
    total_page_row = (total_page + BotConfig.PER_ROW_BUTTON_COUNT - 1) // BotConfig.PER_ROW_BUTTON_COUNT
    # 根据行和列生成对应的页码键盘
    for row in range(0, total_page_row):
        current_row = list()
        for col in range(1, BotConfig.PER_ROW_BUTTON_COUNT + 1):
            if row * BotConfig.PER_ROW_BUTTON_COUNT * page_limit + (col - 1) * page_limit >= len(origin_data_list):
                break
            page = row * BotConfig.PER_ROW_BUTTON_COUNT + col
            current_row.append(InlineKeyboardButton(str(page), callback_data=page))

        keyboard.append(current_row)

        if len(keyboard) >= total_page_row:
            break

    page_data = origin_data_list[(to_page - 1) * page_limit: to_page * page_limit]
    return page_data, keyboard