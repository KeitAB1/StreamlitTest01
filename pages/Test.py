import streamlit as st
import requests


# 定义API类
class FreeApi:
    def __init__(self, keyword):
        self.api_url = f'http://api.qingyunke.com/api.php?key=free&appid=0&msg={keyword}'

    def get_result(self):
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                try:
                    return response.json()  # 解析为JSON
                except ValueError:
                    return {"error": "Response is not valid JSON.", "content": response.text}
            else:
                return {"error": f"Failed to retrieve data. Status code: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}


# 初始化对话历史的 session_state
if 'dialog_history' not in st.session_state:
    st.session_state['dialog_history'] = []

# 页面标题和说明
st.title("智能堆垛问答助手")


# 特殊问题处理函数
def handle_special_questions(user_question):
    if "你是谁" in user_question or "介绍" in user_question:
        return "我是湘潭大学开发的智能钢板堆垛问答助手，为您提供智能问答服务。"
    elif "湘潭大学" in user_question:
        return "湘潭大学是一所具有悠久历史的高等学府，位于中国湖南省。"
    else:
        return None


# 输入框供用户提问
user_question = st.text_input("请输入您的问题:")

# 提交按钮
if st.button("发送"):
    if user_question:
        # 特殊问题的处理
        special_answer = handle_special_questions(user_question)

        if special_answer:
            st.session_state['dialog_history'].append(f"用户: {user_question}")
            st.session_state['dialog_history'].append(f"机器人: {special_answer}")
        else:
            # 调用API获取机器人回复
            api = FreeApi(user_question)
            result = api.get_result()

            if "content" in result:
                response = result['content']
                st.session_state['dialog_history'].append(f"用户: {user_question}")
                st.session_state['dialog_history'].append(f"机器人: {response}")
            elif "error" in result:
                st.session_state['dialog_history'].append(f"错误: {result['error']}")
    else:
        st.error("请输入一个问题！")

# 显示对话历史
if st.session_state['dialog_history']:
    for i, msg in enumerate(st.session_state['dialog_history']):
        if "用户" in msg:
            st.write(f"**{msg}**")  # 用户的消息加粗显示
        else:
            st.write(msg)  # 机器人的回复

