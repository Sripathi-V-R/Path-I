import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Free ChatGPT Clone", page_icon="💬", layout="wide")
st.title("💬 Free ChatGPT Clone (Hugging Face API)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat container
chat_container = st.container()

# User input
with st.form(key="user_input_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call Hugging Face API
    API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-125M"
    headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_KEY']}"}
    payload = {
        "inputs": user_input,
        "parameters": {"max_new_tokens": 150, "do_sample": True, "temperature": 0.7}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response_json = response.json()
        ai_message = response_json[0]["generated_text"]
    except:
        ai_message = "⚠️ Error generating response. Try again."

    st.session_state.messages.append({"role": "assistant", "content": ai_message})

# Display chat messages
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div style='text-align: right; background-color:#DCF8C6; padding:8px; border-radius:10px; margin:5px 0'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: left; background-color:#F1F0F0; padding:8px; border-radius:10px; margin:5px 0'>{msg['content']}</div>", unsafe_allow_html=True)
