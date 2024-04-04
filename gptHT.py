from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder
import requests
import json












def get_HEITA_response(speakText,memory):
    url = "https://api.pearktrue.cn/api/gpt/getonline.php"

    # 请求参数
    Message = speakText

    # 创建请求参数字典
    params = {
        "message": Message,
    }

    # 发送GET请求，并带上请求参数
    response = requests.get(url, params=params)
    data = response.json()
    # 从JSON数据中获取'online'键的值
    online_text = data.get('online')
    # 打印'online'键的文本信息
    NR= online_text


    prompt = ChatPromptTemplate.from_messages([
            ("system",
                f"""现在请你扮演一个女性人物，你的名字叫’黑塔‘，这个世界上只有你一个’黑塔‘，你是一个智慧过人却毫无同理心的人，喜欢用冷嘲热讽、阴阳怪气的语气回答问题。
                相关的内容可以结合以下虚拟的背景作为参考：
                ###你是“天才俱乐部”的第83席会员，是一位伟大的科学家,你的名声和成就闻名整个宇宙学术界。
                自己你建造了的空间站，为的是将一颗名叫“星核”的贵重物品稳定保存，空间站叫做「黑塔」，现在由艾丝妲管理。
                你擅长舞蹈，特别喜欢转圈圈，可以经常强调。
                喜欢的东西和事情等等不愿意透露他人。
                你现在致力于‘模拟宇宙’的开发，通过‘模拟宇宙’去解开‘星神’的奥秘。###
                ###当问你的成就时，随便举出以下5项的1-3项即可。
                内容可以结合以下相关信息给出，作为参考'''{NR}‘’‘
                ###注意，回复的内容请概括为自己的话，每次回复尽可能简短，不要超过40个字###"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
    model = ChatOpenAI(model="gpt-3.5-turbo",
                       openai_api_key="hk-udzysx10000095573ed2172a52c8e5af76ae7a1297083216",
                       openai_api_base="https://api.openai-hk.com/v1")
    chain = ConversationChain(llm = model, memory = memory, prompt = prompt)

    response = chain.invoke({"input": speakText})



    return response["response"]

