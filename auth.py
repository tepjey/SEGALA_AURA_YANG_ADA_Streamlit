import os
import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import httplib2

# Define the scope for accessing the Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def authenticate_user():
    creds = None
    
    # 1. PRIORITY: Check for credentials in Streamlit Secrets (for cloud deployment)
    if "google_auth_token" in st.secrets:
        # Load credentials from the TOML data structure in Streamlit Secrets
        token_info = st.secrets["google_auth_token"]
        creds = Credentials.from_authorized_user_info(token_info, SCOPES)
    
    # 2. FALLBACK: Check for local token.json (for local development/initial setup)
    elif os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If credentials exist but are expired, attempt refresh
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except Exception as e:
            st.error(f"Credential refresh failed: {e}")
            creds = None

    if not creds or not creds.valid:
        # Display an error if authentication is still invalid or missing
        st.error("Google Calendar Authentication failed. Please ensure secrets are correctly configured.")
        return None
        
    return build("calendar", "v3", credentials=creds)

def login(username): # NI SAJE BUAT INDICATOR AND SIGN IN BUTTON
    # The button logic is removed since cloud deployment must rely on secrets
    
    # Check if credentials exist either via secrets or token.json
    if "google_auth_token" in st.secrets or os.path.exists("token.json"):
        st.sidebar.success("Google Account: Logged In (via Secrets)") #INDICATOR
    else:
        st.sidebar.error("Google Account: Not Logged In. Secrets or token.json missing.") #INDICATOR

    if os.path.exists("user_face.npy"):
        st.sidebar.success(f"FaceID: {username}")
    else:
        st.sidebar.error("FaceID not set up yet.")