import streamlit as st
from langchain.memory import ConversationBufferMemory
from gptHT import get_HEITA_response
import base64
# 定义的密码
CORRECT_PASSWORD = "123456"


def check_password():
    # 提示用户输入密码
    password = st.text_input("请输入密码以访问黑塔人偶：")

    # 验证密码是否正确
    if password == CORRECT_PASSWORD:
        st.session_state.is_authenticated = True
        st.success("密码正确，欢迎访问黑塔人偶！")
    else:
        st.error("密码错误，请重试。")
        return False

    return True

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
main_bg('./HEITA11.jpg')

html_title = """  
<h1 style="color: purple;font-size: 10px;">转圈圈~</h1>  
"""

# 使用st.markdown显示HTML标题
st.markdown(html_title, unsafe_allow_html=True)


html_title = """  
<h1 style="color: purple;font-size: 20px;">转圈圈~</h1>  
"""

# 使用st.markdown显示HTML标题
st.markdown(html_title, unsafe_allow_html=True)

st.image('./HEITA4.gif')
html_title = """  
<h1 style="color: purple;font-size: 40px;">💜断线的黑塔人偶💜</h1>  
"""

# 使用st.markdown显示HTML标题
st.markdown(html_title, unsafe_allow_html=True)



    #会话状态
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages = True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "[自动回复]：本人不在空间站，简单事问人偶，麻烦事找艾丝妲解决。"}]

for message in st.session_state["messages"]:
    role = message["role"]
    content = message["content"]

    # 根据角色替换标签
    if role == "ai":
        role_label = "黑塔人偶"  # 自定义的AI角色标签
    elif role == "human":
        role_label = "访客"  # 自定义的人类角色标签
    else:
        role_label = role.upper()  # 对于其他角色，保持原样或转换为大写

    # 使用Markdown来格式化消息
    formatted_message = f"**{role_label}**: {content}"
    st.markdown(formatted_message)


password = st.sidebar.text_input("请输入密码后以访问黑塔人偶：", type='password')



prompt = st.chat_input("请输入你对黑塔的困惑：")

if prompt:
    if password != "123456":
        st.info("请输入访问密码，在左上角")
        st.stop()
    new_message = {"role": "human", "content": prompt}
    st.session_state["messages"].append(new_message)

    # 显示新的人类消息，使用自定义标签
    formatted_message = f"**访客**: {prompt}"
    st.markdown(formatted_message)

    with st.spinner("黑塔小人正在摸鱼💜，请稍等……"):
        response = get_HEITA_response(prompt, st.session_state["memory"])
    st.info("音频加载较慢，会’自动‘播放...（文字越多生成越慢10-30s不等），卡顿请刷新页面")
    audio_file = f"https://df6748bf4f962d130c.gradio.live//?spk=HEITA&text={response}&lang=zh"

    # 创建包含自动播放音频的HTML字符串
    audio_html = f"""  
    <audio controls autoplay>  
        <source src="{audio_file}" type="audio/mpeg">  
        您的浏览器不支持 audio 元素。  
    </audio>  
    """

    # 使用st.components.v1.html来嵌入HTML内容
    st.markdown(audio_html, unsafe_allow_html=True)

    new_ai_message = {"role": "ai", "content": response}
    st.session_state["messages"].append(new_ai_message)

    # 显示新的AI消息
    formatted_ai_message = f"**黑塔人偶**: {response}"
    st.markdown(formatted_ai_message)



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