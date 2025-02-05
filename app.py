# -*- coding: utf-8 -*-

import streamlit as st
from bot import EnglishTeacherBot

def main():
    st.title("🎓 AI English Teacher")
    st.write("Your personal English tutor powered by AI")

    # API key input in sidebar
    with st.sidebar:
        api_key = st.text_input("Enter your DeepSeek API key:", type="password")
        if st.button("Clear Chat History"):
            if 'messages' in st.session_state:
                st.session_state.messages = []
            if 'bot' in st.session_state:
                st.session_state.bot.clear_history()
            st.rerun()

    # Initialize chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        if not api_key:
            st.error("Please enter your DeepSeek API key in the sidebar first!")
            return

        # Initialize bot if not exists
        if 'bot' not in st.session_state:
            st.session_state.bot = EnglishTeacherBot(api_key)

        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.bot.chat(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
