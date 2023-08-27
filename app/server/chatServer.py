import logging

import openai


def get_chat(request) -> str:
    try:
        chartResponse = openai.ChatCompletion.create(

            model="gpt-3.5-turbo",  # 使用第几代GPT

            messages=[

                {"role": "system", "content": "一个问答高手"},  # 设置chartGPT的角色

                {"role": "user", "content": request}  # 设置提问的消息

            ],

        )

        text = chartResponse.get("choices")[0].get('message').get('content')

        logging.info(f"{request} 的回答 {text}")
        return text

    except Exception as e:
        logging.info(f"这次会话可能secretKey过期了 也可能网络故障")
        return "网络通信异常!"