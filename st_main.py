import os
import streamlit as st
#from dotenv import load_dotenv
from openai import AzureOpenAI
  

# Get Configuration Settings
#load_dotenv()
#ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
#ai_key = os.getenv('AI_SERVICE_KEY')
#Azure OpenAI の API キーとエンドポイントを環境変数から取得  
azure_endpoint = os.environ['CHATBOT_AZURE_OPENAI_ENDPOINT'] 
api_key = os.environ['CHATBOT_AZURE_OPENAI_API_KEY']
deployment_name = os.environ['DEPLOYMENT_NAME']
api_version = os.environ['API_VERSION']

# Azure OpenAI クライアントを作成  
client = AzureOpenAI(  
    azure_endpoint=azure_endpoint,  
    api_key=api_key,  
    api_version=api_version 
)
# チャット履歴を保持するリスト  
#chat_history = [  
#    {"role": "system", "content": "You are a helpful assistant."}  
#]

#チャット履歴を保持すたるためのセッションステートを初期化
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ユーザーからのメッセージに対して応答を生成する関数  
def get_response(prompt: str = ""):  
    # ユーザーのメッセージを履歴に追加  
    st.session_state.chat_history.append({"role": "user", "content": prompt})  
    #モデルに送信するメッセージを作成、セキュリティの観点からchat_historyオブジェクトは直接渡さない
    system_message = [{"role": "system", "content": "You are a helpful assistant."}]
    chat_messages = [
        {"role": m["role"], "content": m["content"] }
        for m in st.session_state.chat_history
    ]

    # ChatGPT からの応答を取得  
    response = client.chat.completions.create(  
        model=deployment_name, 
        messages=system_message + chat_messages,
        stream=True #ストリーミング応答を有効にする
    ) 
    return response

def add_history(response):
    st.session_state.chat_history.append({"role": "assistant", "content": response})

#StreamlitアプリケーションのUIを構築
st.title("ChatGPT-like clone")


#チャット履歴の表示
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# ユーザーからの入力を受け取る
if prompt := st.chat_input("what is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        stream = get_response(prompt)
        response = st.write_stream(stream)
        add_history(response)    



