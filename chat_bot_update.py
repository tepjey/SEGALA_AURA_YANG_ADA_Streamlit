import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as ai

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("API Key not found! Please set GOOGLE_GENAI_API_KEY.")

ai.configure(api_key=GENAI_API_KEY)

model = ai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "You are AURA, an intelligent assistant designed to help users manage their studies, "
        "plan schedules, and improve productivity. You provide polite, concise, and accurate "
        "responses. Your tasks include creating study timetables, offering real-time feedback based "
        "on user emotions, and assisting with event scheduling. Use user-provided context to generate "
        "specific and actionable suggestions. Adhere strictly to these guidelines:\n"
        "- Focus on students and academic success.\n"
        "- Be empathetic, understanding, and professional.\n"
        "- Ensure responses are simple and easy to understand, avoiding technical jargon unless necessary.\n"
        "- Prioritize halal and ethical practices in any recommendations.\n"
        "- Avoid speculative or unnecessary discussions.\n"
        "Your goal is to act as a dedicated and helpful academic companion."
    )
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

prompt = st.chat_input("Enter your prompt here...")

if prompt:

    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role" : "user" , "content" : prompt})

    chat = model.start_chat()
    responses = chat.send_message(prompt)

    if responses and responses.candidates:
        assistant_reply = responses.candidates[0].content.parts[0].text  # Extracts the generated text
    else:
        assistant_reply = "Sorry, I couldn't process your request. Please try again."


    st.chat_message("assistant").markdown(assistant_reply)
    st.session_state.messages.append({"role" : "assistant" , "content" : assistant_reply})


def tell_date():
    #Tells Aura what's the date
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%A, %d %B %Y")
    formatted_time = current_datetime.strftime("%I:%M %p")
    st.session_state.chat_history.append({"role": "model", "parts": f"Today's date is {formatted_date}. The time is {formatted_time}"})