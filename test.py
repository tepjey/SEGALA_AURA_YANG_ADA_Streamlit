import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import streamlit as st
import google.generativeai as ai  # Import the Generative AI library
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

# Google Calendar API Setup
SCOPES = ['https://www.googleapis.com/auth/calendar']

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("API Key not found! Please set GOOGLE_GENAI_API_KEY.")

def authenticate_user():
    creds = None
    # Check if token.json exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If no valid credentials, prompt login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)

def fetch_calendar_events(service):
    """Fetch events from Google Calendar."""
    now = datetime.datetime.now().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def ask_generative_ai_to_create_timetable(events):
    """Send events to Google Generative AI to generate a study timetable."""
    ai.configure(api_key=GENAI_API_KEY)  # Replace with your actual API key

    model = ai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=(
            "You are AURA, an intelligent assistant designed to help users manage their studies, "
            "plan schedules, and improve productivity. You provide polite, concise, and accurate "
            "responses. Your tasks include creating study timetables, offering real-time feedback based "
            "on user emotions, assisting with event scheduling and offers personalized advice based on users mood. " 
            "Use user-provided context to generate specific and actionable suggestions. Adhere strictly to these guidelines:\n"
            "- Focus on students and academic success.\n"
            "- Be empathetic, understanding, and professional but casual.\n"
            "- Ensure responses are simple and easy to understand, avoiding technical jargon unless necessary.\n"
            "- Prioritize halal and ethical practices in any recommendations.\n"
            "Your goal is to act as a dedicated and helpful academic companion."
        )
    )
    
    # print(events)
    # Prepare event details for the language model
    event_details = "\n".join(
        [f"{e['summary']} on {e['start'].get('dateTime', e['start'].get('date'))}" for e in events]
    )
    # print(event_details)
    prompt = f"""
    I have the following schedule:
    {event_details}

    Please create a study timetable around these events, ensuring that I have at least 2 hours of study time per day. Focus on balancing study sessions and breaks.
    """

    # Use Generative AI to process the prompt
    chat = model.start_chat()
    response = chat.send_message(prompt)
    
    if response and response.candidates:
        timetable = response.candidates[0].content.parts[0].text  # Extracts the generated text
    else:
        timetable = "Sorry, I couldn't process your request. Please try again."
    
    return timetable

# Authenticate and Fetch Events
if st.button("Generate Timetable"):
    try:
        service = authenticate_user()
        events = fetch_calendar_events(service)
        st.write("Fetched Events:")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            st.write(f"{event['summary']} - {start}")

        # Send to Language Model and Display Timetable
        timetable = ask_generative_ai_to_create_timetable(events)
        st.write("Generated Study Timetable:")
        st.chat_message("bot").markdown(timetable)

    except Exception as e:
        st.error(f"Error: {e}")
