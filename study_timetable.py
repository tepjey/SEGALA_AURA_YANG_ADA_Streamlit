from datetime import datetime, timedelta
from auth import authenticate_user
import streamlit as st

def fetch_upcoming_events(max_results=10):
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

def create_study_timetable(events, study_hours_per_day=2):
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

def display_study_timetable():
    st.header("Study Timetable")
    
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