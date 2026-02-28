import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# .env の読み込み
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit アプリのタイトルと説明
st.title("LLM Chat App with LangChain")
st.write("""
このアプリでは、入力フォームにテキストを入れて送信すると、  
選択した専門家の観点で LLM が回答します。  
ラジオボタンで専門家の種類を選択してください。
""")

# ラジオボタンで専門家の種類を選択
expert_type = st.radio(
    "専門家を選んでください",
    ("医療専門家", "旅行専門家", "IT専門家")
)

# ユーザーの入力フォーム
user_input = st.text_input("質問を入力してください")

# LLMに渡す関数を定義
def get_llm_response(input_text: str, expert: str) -> str:
    # 専門家に応じてシステムメッセージを変更
    if expert == "医療専門家":
        system_msg = "あなたは医療の専門家として、正確かつ分かりやすく回答してください。"
    elif expert == "旅行専門家":
        system_msg = "あなたは旅行の専門家として、具体的なアドバイスをわかりやすく回答してください。"
    elif expert == "IT専門家":
        system_msg = "あなたはITの専門家として、技術的に正確で分かりやすく回答してください。"
    else:
        system_msg = "あなたは親切に回答してください。"

    # LLM にプロンプトを渡す
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name="gpt-4o-mini",
        temperature=0.7
    )

    response = llm([SystemMessage(content=system_msg), HumanMessage(content=input_text)])
    return response.content

# ボタンが押されたら LLM に質問して回答を表示
if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        answer = get_llm_response(user_input, expert_type)
        st.subheader("LLMの回答")
        st.write(answer)