import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import streamlit as st
import time

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Gemini client
client = genai.Client()

def get_mental_health_response(user_input):
    system_prompt = """AI Mental Health Assistant: Provide empathetic support, practical coping strategies, 
    and CBT techniques. Not a therapist. Crisis: 988 or Text HOME to 741741."""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        contents=user_input
    )
    return response.text

# Streamlit settings
st.set_page_config(page_title="🌟 Mental Health Chat", layout="centered")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "waiting_for_ai" not in st.session_state:
    st.session_state.waiting_for_ai = False

st.title("🌟 Mental Health Support Chat")

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")

if st.session_state.waiting_for_ai:
    st.info("AI is typing...")

# Input form
with st.form("chat_form", clear_on_submit=True):
    user_message = st.text_input("Type your message")
    submitted = st.form_submit_button("Send")

if submitted and user_message:
    # Step 1: Show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_message})
    st.session_state.waiting_for_ai = True
    st.rerun()

# Step 2: If waiting for AI, generate response
if st.session_state.waiting_for_ai:
    last_user_message = st.session_state.messages[-1]["content"]
    ai_reply = get_mental_health_response(last_user_message)
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    st.session_state.waiting_for_ai = False
    st.rerun()
