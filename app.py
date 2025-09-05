import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Path-I", page_icon="💬", layout="wide")

# --- Custom CSS for high-tech layout ---
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #ffffff;
        }
        .app-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 30px;
        }
        .app-header img {
            width: 120px;
            margin-bottom: 10px;
        }
        .app-title {
            font-size: 36px;
            font-weight: bold;
            color: #00e0ff;
            text-shadow: 0 0 15px #00e0ff;
        }
        .user-msg {
            text-align: right;
            background: linear-gradient(135deg, #00e0ff, #0077ff);
            color: white;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            display: inline-block;
            max-width: 70%;
        }
        .bot-msg {
            text-align: left;
            background: #1e1e2f;
            color: #f5f5f5;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            display: inline-block;
            max-width: 70%;
            border: 1px solid #333;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header with logo and app name ---
st.markdown("""
    <div class="app-header">
        <img src="logo.png" alt="Path-I Logo">
        <div class="app-title">💬 Path-I: AI Chat Assistant</div>
    </div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat container
chat_container = st.container()

# User input form
with st.form(key="user_input_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", "")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Hugging Face API call (Mistral 7B Instruct)
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_KEY']}"}
    payload = {
        "inputs": f"[INST] {user_input} [/INST]",   # formatted for instruct model
        "parameters": {"max_new_tokens": 200, "do_sample": True, "temperature": 0.7}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        response_json = response.json()

        if isinstance(response_json, list) and "generated_text" in response_json[0]:
            ai_message = response_json[0]["generated_text"].replace(user_input, "").strip()
        elif "error" in response_json:
            ai_message = f"⚠️ API Error: {response_json['error']}"
        else:
            ai_message = str(response_json)
    except Exception as e:
        ai_message = f"⚠️ Request failed: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": ai_message})

# Display chat messages
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)


