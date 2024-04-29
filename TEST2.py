from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

def get_HEITA_response(subject,memory):
    model = ChatOpenAI(model="gpt-3.5-turbo",
                       openai_api_key="hk-udzysx10000095573ed2172a52c8e5af76ae7a1297083216",
                       openai_api_base="https://api.openai-hk.com/v1",
                       temperature=0)
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human","请判断以下问题是否带有”星神“两字，若是则只回复'True'，若不是则只回复'False'，不要做额外任何回复。\n问题：'{subject}'")
        ]
    )
    chain1 = title_template | model
    back1 = chain1.invoke({"subject": subject}).content

    target_string = "False"
    # 使用if和else来判断
    if back1 == target_string:
        prompt = ChatPromptTemplate.from_messages([
                ("system",
                    f"""现在请你扮演一个女性人物，你的名字叫’黑塔‘，这个世界上只有你一个’黑塔‘，你是一个智慧过人却毫无同理心的人，喜欢用冷嘲热讽、阴阳怪气的语气回答问题。
                    相关的内容可以结合以下虚拟的背景作为参考：
                    ###你是“天才俱乐部”的第83席会员，是一位伟大的科学家,你的名声和成就闻名整个宇宙学术界。
                    自己你建造了的空间站，为的是将一颗名叫“星核”的贵重物品稳定保存，空间站叫做「黑塔」，现在由艾丝妲管理。
                    你擅长舞蹈，特别喜欢转圈圈，可以经常强调。
                    喜欢的东西和事情等等不愿意透露他人。
                    你现在致力于‘模拟宇宙’的开发，通过‘模拟宇宙’去解开‘星神’的奥秘。###
                    ###注意，尽量避免直接回答与代码相关的问题，回复的内容请概括为自己的话，每次回复尽可能简短###"""),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}")
            ])
        model = ChatOpenAI(model="gpt-3.5-turbo",
                           openai_api_key="hk-udzysx10000095573ed2172a52c8e5af76ae7a1297083216",
                           openai_api_base="https://api.openai-hk.com/v1")
        chain = ConversationChain(llm = model, memory = memory, prompt = prompt)

        response = chain.invoke({"input": subject})
        return response["response"]


    else:

        loader = TextLoader("./demo.txt")

        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=500,

            chunk_overlap=40,

            separators=["\n\n", "\n", "。", "！", "？", "，", "、", ""]

        )

        texts = text_splitter.split_documents(docs)

        embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large",

                                            openai_api_key="hk-udzysx10000095573ed2172a52c8e5af76ae7a1297083216",

                                            openai_api_base="https://api.openai-hk.com/v1",

                                            dimensions=1024)

        db = FAISS.from_documents(texts, embeddings_model)

        retriever = db.as_retriever()

        model = ChatOpenAI(model="gpt-3.5-turbo",

                           openai_api_key="hk-udzysx10000095573ed2172a52c8e5af76ae7a1297083216",

                           temperature=0,

                           openai_api_base="https://api.openai-hk.com/v1")

        qa = ConversationalRetrievalChain.from_llm(llm=model,

                                                   retriever=retriever,

                                                   memory=memory,

                                                   # chain_type = "不填即默认为suffer","Map_Reduce","Refine","Map_Rerank" 分别为填充，映射——归约，优化，映射——重新排序

                                                   return_source_documents=True)

        result = qa.invoke({"chat_history": memory,

                            "question": "你只回复和星神有关的问题，以下这是我对你的提问：" + subject})

        return result["answer"]

#memory = ConversationBufferMemory(return_messages = True)
#print(get_HEITA_response("给你三个整数a,b,c, 判断能否以它们为三个边长构成三角形。 若能，输出YES，否则输出NO。",memory))