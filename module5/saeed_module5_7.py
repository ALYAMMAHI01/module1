st.session_state
import streamlit as st

st.set_page_config(page_title="Chat with Memory", layout="centered")

st.title("LLM Chat (With Memory)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Say something...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    response = f"I remember you said: {user_input}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.markdown(response)
