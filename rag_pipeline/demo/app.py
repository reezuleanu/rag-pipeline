import os

import streamlit as st
import streamlit_authenticator as stauth
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI

# keep index in memory
index = None

# get username and hashed password from env
credentials = {
    "usernames": {os.environ["USERNAME"]: {"password": os.environ["PASSWORD"]}}
}

authenticator = stauth.Authenticate(
    credentials,
    "rag_pipeline_cookie",
    "rag_pipeline",
)

if auth_tuple := authenticator.login("main"):
    # print(auth_tuple)
    pass

authenticator.logout(location="sidebar")


def init_index():
    global index
    if index is None:
        index = VectorStoreIndex.from_documents([])
    return index


def render_chat():
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)


st.title("🦙 RAG demo with LlamaIndex")

if "chat_engine" not in st.session_state:
    llm = OpenAI(
        # model="gpt-4o",
        temperature=0.1,
        streaming=True,
    )
    index = init_index()
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="simple", llm=llm, verbose=True
    )
    st.session_state.chat_history = [("ai", "Hi, how can i help you?")]
    render_chat()

if not st.session_state.get("is_generating", False):
    prompt = st.chat_input("Have any questions?")
else:
    prompt = st.chat_input("The bot is answering...", disabled=True)


if prompt:
    st.session_state.is_generating = True
    st.session_state.chat_history.append(("user", prompt))
    render_chat()
    response = st.session_state.chat_engine.stream_chat(prompt)
    with st.chat_message("ai"):
        final_response = st.write_stream(response.response_gen)
    st.session_state.chat_history.append(("ai", str(final_response)))
    st.session_state.is_generating = False
