import streamlit as st
from langchain.memory import ConversationBufferWindowMemory
from gptHT import get_HEITA_response
import base64
import time
import pygame
import threading
import requests
import io
# 定义的密码
CORRECT_PASSWORD = "123456"


def play_audio_from_api(api_url):
    # 使用requests从API获取音频数据
    response = requests.get(api_url)

    # 确保请求成功
    if response.status_code == 200:
        audio_data = response.content

        # 将音频数据转换为BytesIO对象
        audio_stream = io.BytesIO(audio_data)

        # 初始化pygame的mixer模块
        pygame.mixer.init()

        # 加载音频流
        pygame.mixer.music.load(audio_stream)

        # 播放音频
        pygame.mixer.music.play()

        # 等待音频播放完毕
        while pygame.mixer.music.get_busy():
            continue

            # 清理资源
        pygame.mixer.quit()
    else:
        print(f"Error fetching audio from API: {response.status_code}")

        # 设置API的URL


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
main_bg('./HEITA100.jpg')








html_title = """  
<h1 style="color: purple;font-size: 20px;">转圈圈小游戏80满分(游戏期间请勿点击其他操作~</h1>  
"""

# 使用st.markdown显示HTML标题
st.markdown(html_title, unsafe_allow_html=True)



# 初始化pygame混音器模块
pygame.mixer.init()

# 定义音频文件及其播放的次数范围
audio_ranges = {
    '转圈圈.mp3': range(1, 16),  # 第1次到第4次点击播放audio1.mp3
    'gururu.mp3': range(16, 41),  # 第5次到第9次点击播放audio2.mp3
    '转圈圈咯.mp3': range(41, 61),  # 第10次到第15次点击播放audio3.mp3
    'gululu.mp3': range(61, 77),
    '要坏掉了.mp3': range(77, 80),
    # 你可以根据需要添加更多音频文件及其范围
}

# 定义一个字典来存储音频文件是否已加载的状态
audio_loaded = {}


# 定义一个函数来加载音频文件
def load_audio(audio_path):
    if audio_path not in audio_loaded or not audio_loaded[audio_path]:
        pygame.mixer.music.load(audio_path)
        audio_loaded[audio_path] = True

    # 定义播放音频的函数


def play_audio(audio_path):
    load_audio(audio_path)  # 确保音频已加载
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue  # 等待音频播放完毕


def main():
    # 如果计数器尚未初始化，则初始化为0
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
        st.session_state.current_image = '0.jpg'
    if 'B' not in st.session_state:
        st.session_state['B'] = 0
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = None

            # 显示当前计数器的值


    # 创建一个按钮来播放音频并计数
    if st.button('来和黑塔转圈圈吧~'):
        # 增加计数器的值
        if st.session_state.counter<80 and st.session_state['B']<80:
            st.session_state.counter += 1

        if st.session_state['start_time'] is None:
            st.session_state['start_time'] = time.time()
    current_time = time.time()

    if st.session_state['start_time'] is not None:
        elapsed_time = current_time - st.session_state['start_time']
        # 假设每过一秒，B的值增加1（你可以根据需要调整这个增长速率）
        if st.session_state['B']<=80 and st.session_state.counter<=80:
            if elapsed_time <= 10:
                st.session_state['B'] = int(elapsed_time*2)
            elif 10 < elapsed_time <= 20:
                st.session_state['B'] = int(20+(elapsed_time-10)*3)
            elif 20 < elapsed_time <=30:
                st.session_state['B'] = int(55+(elapsed_time-20)*5)



    st.write(f'你的当前得分: {st.session_state.counter}')
    st.write('黑塔的得分:', st.session_state['B'])
    # 根据计数器的值更新图片路径
    if 1 <= st.session_state.counter <= 15:
        st.session_state.current_image = '1.gif'  # 10次点击时的图片
        st.write("黑塔认为自己势在必得~")
    elif 15 < st.session_state.counter <= 40:
        st.session_state.current_image = '2.gif'  # 20次点击时的图片
        st.write("黑塔人偶开始高速转动了！")
    elif 40 < st.session_state.counter < 80:
        st.session_state.current_image = '3.gif'  # 30次点击时的图片
        st.write("黑塔人偶已全功率启动！！！")
    elif 80 <= st.session_state.counter :
        st.session_state.current_image = '4.jpg'  # 5次到29次点击时的图片
        st.write("黑塔转吐了，你赢了。（刷新以继续）")
    else:
        st.session_state.current_image = '0.jpg'  # 少于5次点击时的图片
        st.write("黑塔认为稳操胜券，不把你放在眼里")

    if st.session_state.counter > st.session_state['B']:
        st.success('你超过黑塔了!')
    elif st.session_state.counter < st.session_state['B']:
        st.error('黑塔超过你了!')
    else:
        st.warning('你们不分上下!')

    if st.session_state.counter>=80 and st.session_state['B'] < 80:
            st.title("你赢了！")
    elif st.session_state.counter < 80 and st.session_state['B'] >= 80:
            st.title("黑塔赢了！")
    elif st.session_state.counter==st.session_state['B']==80:
            st.title("平局")


        # 根据计数器的值播放相应的音频文件
    for audio_path, range_ in audio_ranges.items():
        if st.session_state.counter in range_:
            # 使用线程来播放音频，防止阻塞Streamlit的事件循环
            threading.Thread(target=play_audio, args=(audio_path,), daemon=True).start()
            break  # 找到匹配的音频范围后退出循环

    # 显示图片
    st.image(st.session_state.current_image)


if __name__ == '__main__':
    main()

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

# 假设您已经有了一个ConversationBufferMemory类和get_chat_response函数


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
    background-color: #f2f2f2;  
}  

.message-box.ai {  
    background-color: #e0e0ff;  
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
password = st.sidebar.text_input("请输入密码后以访问黑塔人偶：", type='password')
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

        api_url = f"https://9b98eba910d46bae6c.gradio.live//?spk=HEITA&text={response}&lang=zh"
        # 调用函数播放音频
        play_audio_from_api(api_url)
        # 将AI的响应添加到历史记录并显示
    st.session_state["messages"].append({"role": "ai", "content": response})
    # 使用新的标签文本渲染AI响应
    role_label_text = role_labels["ai"]
    html_message = f'<div class="message-box ai"><span class="role-label">{role_label_text}:</span> {response}</div>'
    st.markdown(html_message, unsafe_allow_html=True)