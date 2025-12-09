# NI AUTHENTICATION

import os
import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scope for accessing the Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]

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

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    st.sidebar.success("Google Account: Logged In")
else:
    if st.sidebar.button("Login", type="primary"):
        authenticate_user()
        st.sidebar.success("Google Account: Log in Successful")

# ------------------------------------------------------------------------------------------------
# NI SMUA BENDA PASAL CALENDAR

from datetime import datetime, timedelta
from auth import authenticate_user
import streamlit as st

def displaycalendar(): # NI NAK DISPLAY CALENDAR (KENA UBAH)
    st.info("Fetching upcoming events from your Google Calendar...")
    
    try:
        # Fetch upcoming events
        events = fetch_upcoming_events()
        
        if not events:
            st.warning("No upcoming events found!")
            return
        
        # Create study timetable
        timetable = create_study_timetable(events)
        
        if not timetable:
            st.warning("Unable to generate timetable!")
            return
        
        # Display timetable
        for date, tasks in sorted(timetable.items()):
            st.subheader(f"{date.strftime('%A, %d %B %Y')}")
            for task in tasks:
                st.write(f"• {task}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def fetch_upcoming_events(max_results=10): # NI UNTUK FETCH UPCOMING EVENTS
    try:
        service = authenticate_user()
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(
            calendarId='primary', timeMin=now, maxResults=max_results, singleEvents=True,
            orderBy='startTime').execute()
        return events_result.get('items', [])
    except Exception as e:
        print(f"An error occurred while fetching events: {e}")
        return []

def create_study_timetable(events, study_hours_per_day=2): # NI UNTUK CREATE TIME TABLE (TARIKH EVENT TOLAK 2 HARI) (JAGNAN BUAT MANUAL MCMNI, MINTAK GEMINI BUAT LEPASTU DISPLAY)
    timetable = {}
    try:
        for event in events:
            event_name = event.get('summary', 'Unnamed Event')
            event_start = datetime.fromisoformat(event['start']['dateTime'])
            
            # Calculate preparation start date (e.g., 2 days before the event)
            prep_start = event_start - timedelta(days=2)
            
            # Allocate study sessions between prep_start and event_start
            current_date = prep_start
            while current_date < event_start:
                if current_date.date() not in timetable:
                    timetable[current_date.date()] = []
                timetable[current_date.date()].append(f"Study for {event_name} ({study_hours_per_day} hrs)")
                current_date += timedelta(days=1)
        return timetable
    except Exception as e:
        print(f"An error occurred while creating the timetable: {e}")
        return {}

if __name__ == "__main__":
    # Fetch upcoming events
    events = fetch_upcoming_events()
    
    # Create study timetable
    timetable = create_study_timetable(events)
    
    # Print timetable
    for date, tasks in sorted(timetable.items()):
        print(f"{date}:")
        for task in tasks:
            print(f"  - {task}")