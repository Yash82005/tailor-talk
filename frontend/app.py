import streamlit as st
import requests

st.title("TailorTalk Chatbot")

user_input = st.text_input("What can I help you with?")

if st.button("Submit") and user_input:
    try:
        response = requests.post("https://tailor-talk-v3nx.onrender.com/agent", json={"query": user_input})
        st.write("Status Code:", response.status_code)
        st.write("Raw Response:", response.text)  # 👈 Add this to debug
        st.write("Bot Reply:", response.json()["reply"])
    except Exception as e:
        st.error(f"Something went wrong: {e}")
