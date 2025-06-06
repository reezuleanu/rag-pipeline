import streamlit as st
import streamlit_authenticator as stauth
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.opensearch import (
    OpensearchVectorClient,
    OpensearchVectorStore,
)
from llama_index.llms.openai import OpenAI

from rag_pipeline.settings import settings

# keep index in memory
index = None


def init_index():
    global index
    if index is None:
        opensearch_client = OpensearchVectorClient(
            endpoint=settings.OPENSEARCH_ENDPOINT,
            index=settings.OPENSEARCH_INDEX,
            dim=1536,
            verify_certs=False,  # ignore self signed certs
            ssl_show_warn=False,
            http_auth=(settings.OPENSEARCH_USERNAME, settings.OPENSEARCH_PASSWORD),
        )
        index = VectorStoreIndex.from_vector_store(
            OpensearchVectorStore(opensearch_client)
        )
    return index


# get username and hashed password from env
credentials = {
    "usernames": {settings.APP_USERNAME: {"password": settings.APP_PASSWORD}}
}

authenticator = stauth.Authenticate(
    credentials,
    "rag_pipeline_cookie",
    "rag_pipeline",
)


if st.session_state.get("authentication_status") is None:
    authenticator.login("main")

elif st.session_state.get("authentication_status") is False:
    authenticator.login("main")
    st.error("Username/password is incorrect")

elif st.session_state.get("authentication_status"):

    def render_chat():
        for role, message in st.session_state.chat_history:
            with st.chat_message(role):
                st.markdown(message)

    st.title("🦙 RAG demo with LlamaIndex")

    if "chat_engine" not in st.session_state:
        llm = OpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            streaming=True,
        )
        index = init_index()
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="best", llm=llm, verbose=True
        )
        st.session_state.chat_history = [("ai", "Hi, how can i help you?")]
    render_chat()

    prompt = st.chat_input("Have any questions?")

    if prompt:
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
        response = st.session_state.chat_engine.stream_chat(prompt)
        with st.chat_message("ai"):
            final_response = st.write_stream(response.response_gen)
        st.session_state.chat_history.append(("ai", str(final_response)))
