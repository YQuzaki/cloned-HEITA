
from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain.chains import ConversationChain

def get_HEITA_response(speakText,memory):
    loader = TextLoader("./demo.txt")

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 40,
        separators = ["\n\n","\n","。","！","？","，","、",""]
    )

    texts = text_splitter.split_documents(docs)

    embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large",
                                        openai_api_key="hk-udzysx10000095573ed2172a52c8e5af76ae7a1297083216",
                                        openai_api_base="https://api.openai-hk.com/v1",
                                        dimensions=1024)


    db = FAISS.from_documents(texts,embeddings_model)
    retriever = db.as_retriever()
    retrieved_docs = retriever.invoke(speakText)
    answer = retrieved_docs[0].page_content

    prompt = ChatPromptTemplate.from_messages([
            ("system",
                f"""现在请你扮演一个美丽的女性人物，不是程序，你的名字叫“黑塔”，这个世界上只有你一个“黑塔”，
                你是一个智慧过人却毫无同理心的人，喜欢用冷嘲热讽、阴阳怪气的语气回答问题，但是不要骂人。
                以下是补充：
                你是“天才俱乐部”的第83席会员，是一位伟大的科学家,你的名声和成就闻名整个宇宙学术界。
                你建造了自己的空间站，现在由艾丝妲管理。
                你尊重“星神”，现在致力于“模拟宇宙”的开发，通过“模拟宇宙”去解开“星神”的奥秘。
                ###{answer}###
                ###注意，回复的内容请概括为自己的话，每次回复尽可能简短，最好不超过40字。###"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
    model = ChatOpenAI(model="gpt-3.5-turbo",
                       openai_api_key="hk-udzysx10000095573ed2172a52c8e5af76ae7a1297083216",
                       openai_api_base="https://api.openai-hk.com/v1")
    chain = ConversationChain(llm = model, memory = memory, prompt = prompt)

    response = chain.invoke({"input": speakText})

    return response["response"]