# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import openai
import streamlit as st
from streamlit_config import streamlit_config

init_config = streamlit_config()

assert 'OPENAI_API_KEY' in st.secrets, "OPENAI_API_KEY not found in secrets."

openai.api_key = st.secrets['OPENAI_API_KEY']

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# def clear_chat_history():
#    st.session_state.messages = [
#        {"role": "assistant", "content": "How may I assist you today?"}]
# st.button('Clear Chat History', on_click=clear_chat_history)


if prompt := st.chat_input("Message ChatGPT..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages], stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
