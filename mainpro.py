import streamlit as st
import json
from PIL import Image
from auth import login
from add_event import submit_event
from streamlit_option_menu import option_menu
from emotion_page import detect_emotion, display_emotion_feedback, detect_emotion_pro
from aura import showaura, homepage, startfeg, generatett
from setup_face_id import mainfaceid
import os
from streamlit_lottie import st_lottie

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Initialize session state for username
if "username" not in st.session_state:
    st.session_state.username = ""

st.set_page_config(
        page_title="AURA",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
logo = Image.open("auralogo_glow.png")
st.sidebar.image(logo, use_container_width=True)
st.sidebar.text(" ")
st.sidebar.text(" ")

with st.sidebar:
    selected_section = option_menu(
        menu_title="Main",
        options=[
            "AURA Home",
            "FaceID Setup",
            "Your Calendar",
            "Emotion Detection",
            "AURA ChatBot",
        ],
        icons=[
            "house",
            "person-bounding-box",
            "calendar-event",
            "emoji-smile-fill",
            "person-fill",
        ],
        menu_icon="list",
        default_index=0,
        styles={
            "menu_title": {"font-size": "15px"},
            "container": {"padding": "5px", "background-color": "#0e1117"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "--hover-color": "#e2d7f4",
            },
            "nav-link-selected": {"background-color": "#ac94f4"},
        },
    )

if selected_section == "AURA Home":
    st.sidebar.markdown("### Useful Links")
    st.sidebar.markdown(
        """
        - [📄 Documentation](https://example.com)
        - [💬 Support](https://example.com/support)
        - [⭐ Rate Us](https://example.com/rate)
        """
    )
    homepage()

elif selected_section == "FaceID Setup":
    mainfaceid()

elif selected_section == "Your Calendar":
    st.sidebar.link_button("Open Google Calendar", "https://calendar.google.com/")
    login(st.session_state.username)

    # Center the title using Streamlit HTML and CSS
    st.markdown(
        "<h1 style='text-align: center;'>Your Calendar 📅</h1>",
        unsafe_allow_html=True,
    )
    st.markdown("")

    # Create two columns for subheaders
    col1, col2 = st.columns(2)

    # Add content to the left column
    with col1:
        submit_event()

    # Add content to the right column
    with col2:
        with st.form("create_timetable"):
            st.header("Create Study Timetable ⏰")
            st.markdown("Press the button below to start creating your study timetable.")
            st.markdown("")
            submitted = st.form_submit_button("Generate Timetable")

            if submitted:
                try:
                    generatett()
                except Exception as e:
                    st.error(f"An error occurred: {e}")

elif selected_section == "Emotion Detection":
    st.title("Emotion Detection 😊")
    st.markdown(
    """
    <style>
    .emotion-btn {
        background-color: #FFA586;
        border: none;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
    }
    .emotion-btn:hover {
        background-color: #B51A2B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    start = st.button("Start Emotion Detection", key="detect")
    if start:
        with st.spinner("Detecting your emotion..."):
            last_emotion = detect_emotion_pro()
        display_emotion_feedback(last_emotion)

elif selected_section == "AURA ChatBot":
    clear = st.sidebar.button("Clear Chat", key="clear")
    if clear:
        st.session_state.messages = []

    if os.path.exists("user_face.npy"):
        login(st.session_state.username) #SIDEBAR AND AUTH
        showaura(st.session_state.username) 
        start = st.sidebar.button("Start Aura", key="start")
        if start:
            startfeg(st.session_state.username) #START AURA TO DETECT USER AND GREET THEM
    else:
        st.error("Please set up your FaceID and enter your nickname in the previous section.")