from datetime import datetime, timedelta
from auth import authenticate_user
import streamlit as st

def add_event_to_calendar(summary, description, start_date, end_date, reminder_minutes):
    try:
        # Get the Google Calendar service
        service = authenticate_user()

        # Define the event
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_date.isoformat(),
                'timeZone': 'Asia/Kuala_Lumpur',
            },
            'end': {
                'dateTime': end_date.isoformat(),
                'timeZone': 'Asia/Kuala_Lumpur',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': reminder_minutes},
                    {'method': 'popup', 'minutes': reminder_minutes},
                ],
            },
        }

        # Insert the event
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {created_event.get('htmlLink')}")
    except Exception as e:
        print(f"An error occurred: {e}")

def submit_event():
    # Input form for adding an event
    
    with st.form("add_event_form"):
        st.header("Event To Your Calendar 📆")
        st.markdown("Use the form below to add an event to your Google Calendar.")
        st.markdown("")
        event_name = st.text_input("Event Name", placeholder="Enter the event name")
        event_date = st.date_input("Event Date")
        event_time = st.time_input("Event Time")
        event_duration = st.number_input("Event Duration (hours)", min_value=1, max_value=12, value=2)
        reminder_minutes = st.number_input("Reminder (minutes before)", min_value=5, max_value=1440, value=60)
        submitted = st.form_submit_button("Add Event")

        if submitted:
            try:
                start_datetime = datetime.combine(event_date, event_time)
                end_datetime = start_datetime + timedelta(hours=event_duration)
                add_event_to_calendar(
                    summary=event_name,
                    description=f"Reminder for {event_name}",
                    start_date=start_datetime,
                    end_date=end_datetime,
                    reminder_minutes=reminder_minutes,
                )
                st.success("Event added successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")