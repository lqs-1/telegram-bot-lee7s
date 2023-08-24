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
        return chartResponse.get("choices")[0].get('message').get('content')

    except Exception as e:
        return "网络通信异常!"