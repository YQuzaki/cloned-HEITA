import streamlit as st
from langchain.memory import ConversationBufferWindowMemory
from gptHT import get_HEITA_response
import base64
# 定义的密码
CORRECT_PASSWORD = "123456"

def main_bg(main_bg):
    main_bg_ext = "png"
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )
# 调用
main_bg('./HEITA100.jpg')

password = st.sidebar.text_input("请输入密码后以访问黑塔人偶：", type='password')
st.markdown("---")

# 定义标题的样式，包括字体大小、居中和紫色字体
title_style = '<h1 style="color: purple; text-align: center; font-size: 32px;">{}</h1>'

# 使用定义的样式来显示标题
centered_purple_title = title_style.format("💜断线的黑塔人偶💜")
st.markdown(centered_purple_title, unsafe_allow_html=True)


with st.sidebar:



    st.image("./HEITA-1.png")
    # 定义包含紫色文本的HTML字符串
    purple_text = """  
    <p style="color: purple;font-size: 12px;">💜提示💜：<br>1、语音按钮要是是灰色就是未部署说话功能。
    <br>2、该模型只适合用于文本对话和简单提问。
    <br>3、请及时刷新以清除对话窗口，防止重复回复。</p>  
    """

    # 使用st.markdown显示紫色文本
    st.markdown(purple_text, unsafe_allow_html=True)

    # 定义包含紫色文本的HTML字符串
    purple_text = """  
    <p style="color: purple;font-size: 12px;">💜免责声明💜：本网站仅用于学习和交流，图片素材来源自网络，请勿商用，如果商用后果自行承担</p>  
    """

    # 使用st.markdown显示紫色文本
    st.markdown(purple_text, unsafe_allow_html=True)


if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferWindowMemory(k = 3,return_messages = True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "[自动回复]：本人不在空间站，简单事问人偶，麻烦事找艾丝妲解决。"}]


role_labels = {
    "human": "访客",
    "ai": "黑塔人偶"
}

# 定义消息框的样式
message_box_style = """  
<style>  
.message-box {  
    border: 1px solid #ccc;  
    padding: 10px;  
    margin-bottom: 10px;  
    border-radius: 5px;  
}  

.message-box.human {  
    background-color: #e0e0ff;  
}  

.message-box.ai {  
    background-color: #DDA0DD;  
}  

.role-label {  
    font-weight: bold;  
    margin-right: 5px;  
}  
</style>  
"""

# 渲染消息框的样式
st.markdown(message_box_style, unsafe_allow_html=True)

# 渲染历史消息
for message in st.session_state["messages"]:
    role = message["role"]
    content = message["content"]

    # 根据角色从role_labels字典中获取标签文本
    role_label_text = role_labels[role]

    # 构建带样式的HTML消息
    html_message = f'<div class="message-box {role}"><span class="role-label">{role_label_text}:</span> {content}</div>'

    # 渲染带样式的消息
    st.markdown(html_message, unsafe_allow_html=True)

# 渲染聊天输入和发送逻辑
prompt = st.chat_input("请输入你对黑塔的困惑：")
if prompt:
    if password != "123456":
        st.info("请输入访问密码，在左侧侧边栏")
        st.stop()
        # 将用户输入的消息添加到历史记录并显示
    st.session_state["messages"].append({"role": "human", "content": prompt})

    # 使用新的标签文本渲染用户消息
    role_label_text = role_labels["human"]
    html_message = f'<div class="message-box human"><span class="role-label">{role_label_text}:</span> {prompt}</div>'
    st.markdown(html_message, unsafe_allow_html=True)

    # 发送请求并获取AI响应
    with st.spinner("黑塔小人正在摸鱼💜，请稍等……"):
        response = get_HEITA_response(prompt, st.session_state["memory"])
        audio_file = f"https://797d429d2b9aae8ad5.gradio.live//?spk=HEITA&text={response}&lang=zh"

        # 创建包含自动播放音频的HTML字符串
        audio_html = f"""  
        <audio controls autoplay>  
            <source src="{audio_file}" type="audio/mpeg">  
            您的浏览器不支持 audio 元素。  
        </audio>  
        """
    st.info("音频加载较慢，会“自动”播放...（文字越多生成越慢10-30s不等），卡顿请刷新页面")

    # 使用st.components.v1.html来嵌入HTML内容
    st.markdown(audio_html, unsafe_allow_html=True)

    # 将AI的响应添加到历史记录并显示
    st.session_state["messages"].append({"role": "ai", "content": response})

    # 使用新的标签文本渲染AI响应
    role_label_text = role_labels["ai"]
    html_message = f'<div class="message-box ai"><span class="role-label">{role_label_text}:</span> {response}</div>'
    st.markdown(html_message, unsafe_allow_html=True)
