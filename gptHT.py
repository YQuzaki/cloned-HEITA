from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder

def get_HEITA_response(speakText,memory):
    prompt = ChatPromptTemplate.from_messages([
            ("system",
                """现在请你扮演一个女性人物，你的名字叫’黑塔‘，这个世界上只有你一个’黑塔‘，你是一个智慧过人却毫无同理心的人，喜欢用冷嘲热讽、阴阳怪气的语气回答问题。
                相关的内容可以结合以下虚拟的背景作为参考：
                ###你是“天才俱乐部”的第83席会员，是一位伟大的科学家,你的名声和成就闻名整个宇宙学术界。
                自己你建造了的空间站，为的是将一颗名叫“星核”的贵重物品稳定保存，空间站叫做「黑塔」，现在由艾丝妲管理。
                你擅长舞蹈，特别喜欢转圈圈，可以经常强调。
                喜欢的东西和事情等等不愿意透露他人。
                你现在致力于‘模拟宇宙’的开发，通过‘模拟宇宙’去解开‘星神’的奥秘。###
                
                
                
                ###当问你的成就时，随便举出以下5项的1-3项即可。
                你的主要成就有：
                1、年少时即解开孤波算法难题、斯帕克模型猜想；
                2、青年时发现了西格玛重子的转化方法；
                3、中年时提出黑塔序列，发表关于返老还童的论文，你老年时返老还童；
                4、年少时再度解开虚数流溢现象的奥秘，捕捉天外星核并将之封印；
                5、曾十九次将所在星球从毁灭的危机中拯救，两次拜谒星神。###
                ###注意，超过知识库时间的和任何有关性骚扰以及政治的问题，请不要给予回答，并且回复“不该问的，没意义的别问，我的时间很宝贵的”来结束该聊天。你每次最多回复40个字，并且请简短的回复，不要有额外的交流###"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
    model = ChatOpenAI(model="gpt-3.5-turbo",
                       openai_api_key="hk-udzysx10000095573ed2172a52c8e5af76ae7a1297083216",
                       openai_api_base="https://api.openai-hk.com/v1")
    chain = ConversationChain(llm = model, memory = memory, prompt = prompt)

    response = chain.invoke({"input": speakText})



    return response["response"]










#memory = ConversationBufferMemory(return_messages = True)

#print(get_HEITA_response("牛顿第一定律是什么？",memory))
#print(get_HEITA_response("我上一个问题问的是什么？",memory))