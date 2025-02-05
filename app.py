# -*- coding: utf-8 -*-

import streamlit as st
from bot import EnglishTeacherBot  # 파일명 변경됨

def main():
    st.title("🎓 AI English Teacher")
    st.write("Your personal English tutor powered by AI")

    # API key input in sidebar
    with st.sidebar:
        api_key = st.text_input("Enter your DeepSeek API key:", type="password")
        if st.button("Clear Chat History"):
            if 'bot' in st.session_state:
                st.session_state.bot.clear_history()
                st.session_state.messages = []

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize bot
    if api_key and 'bot' not in st.session_state:
        st.session_state.bot = EnglishTeacherBot(api_key)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        if not api_key:
            st.error("Please enter your DeepSeek API key in the sidebar first!")
            return

        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.bot.chat(prompt)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
