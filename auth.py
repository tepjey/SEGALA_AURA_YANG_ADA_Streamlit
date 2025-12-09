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
    # Check for credentials in Streamlit Secrets (for cloud deployment)
    if "google_auth_token" in st.secrets:
        from google.auth import impersonated_credentials, default
        from google.auth.transport.requests import Request
        
        # Load credentials from the TOML data structure in Streamlit Secrets
        token_info = st.secrets["google_auth_token"]
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)
    
    # Check for local token.json (for local development/initial setup)
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If credentials exist but are expired, attempt refresh
    if creds and creds.expired and creds.refresh_token:
        # Note: Request() is imported at the top of the file
        creds.refresh(Request())

    if not creds or not creds.valid:
        st.error("Authentication failed. Google Calendar features disabled.")
        return None
        
    return build("calendar", "v3", credentials=creds)

# ALSO UPDATE login() function to avoid running authenticate_user() on button press
def login(username):
    # This function is now simplified to only check for credentials
    if os.path.exists("token.json") or "google_auth_token" in st.secrets:
        st.sidebar.success("Google Account: Logged In (via Secrets)")
    else:
        st.sidebar.error("Google Account: Not Logged In. Secrets missing.")

    if os.path.exists("user_face.npy"):
        st.sidebar.success(f"FaceID: {username}")
    else:
        st.sidebar.error("FaceID not set up yet.")