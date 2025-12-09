import json
import streamlit as st
from streamlit_lottie import st_lottie
import os
from dotenv import load_dotenv
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs
import time
from PIL import Image
from datetime import datetime
import google.generativeai as ai
import cv2
import face_recognition
import numpy as np
from deepface import DeepFace
import webview
import threading
from multiprocessing import Process
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Google Calendar API Setup
SCOPES = ['https://www.googleapis.com/auth/calendar']

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("API Key not found! Please set GOOGLE_GENAI_API_KEY.")
ai.configure(api_key=GENAI_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def jessay(t2sjess):
    load_dotenv()
    client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_KEY"),
    )
    audio = client.generate(
            text=t2sjess,
            voice=Voice(
                voice_id='cgSgspJ2msm6clMCkdW9',
                settings=VoiceSettings(stability=0.4, similarity_boost=0.3, style=1.0, use_speaker_boost=True)
            )
        )
    #play(audio)

def showaura(username):
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)

    lottie_aura = load_lottiefile("lottiefiles/aurarobot.json")

    col1, col2 = st.columns([0.8,1.5])

    with col2:
        st.markdown(
            """
            <style>
            .lottie-container {
                text-align: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st_lottie(lottie_aura, height=350, width=350, key="robot", quality="high",)

    with col1:
        st.markdown(
            """
            <div>
                <h1></h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    chat_bot(username)

def intro_layout():# NOT USING
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)

    lottie_aura = load_lottiefile("lottiefiles/aurarobot.json")

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
        .futuristic {
            font-family: 'Orbitron', sans-serif;
            color: #FFA586;
        }
        .subtext {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2em;
            color: #FFFFFF;
            line-height: 1.8;
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        button {
            background-color: #FFA586;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-family: Orbitron, sans-serif;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns([0.5,1.5])

    with col1:
        st_lottie(
            lottie_aura,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=350,
            width=350,
            key="intro_animation",
        )

    with col2:
        st.markdown(
            """
            <div>
                <h1 class="futuristic">✨ AURA: Pembantu Pintar Pembelajaran Peribadi ✨</h1>
                <p class="subtext">
                    AURA is your <b>personalized desk buddy</b>, here to elevate your productivity and make your study sessions fun and efficient.
                </p>
                <ul class="subtext">
                    <li>🧠 Detects and responds to <b>your emotions</b></li>
                    <li>⏰ Helps you <b>manage your time and schedules</b></li>
                    <li>📚 Acts as your <b>planner and study assistant</b></li>
                </ul>
                <p class="subtext">
                    Start your journey with AURA today and <b>unleash your potential!</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

def homepage():
    # CSS for Custom Styling
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
        body {
            background: linear-gradient(135deg, #384358, #0e1117);
            animation: gradient-animation 5s infinite;
        }
        @keyframes gradient-animation {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
        .main-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 40px;
            color: #FFA586;
            text-align: center;
            margin-bottom: 10px;
            margin-top: -30px;
            animation: fadeIn 2s ease-in-out;
        }
        .tagline {
            text-align: center;
            color: #A6A6A6;
            font-size: 18px;
            margin-bottom: 40px;
            animation: fadeIn 2s ease-in-out;
        }
        .feature-box {
            background-color: #384358;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
            animation: fadeIn 2s ease-in-out;
        }
        .feature-box h4 {
            color: #F5C10F;
            margin-bottom: 10px;
            animation: fadeIn 2s ease-in-out;
        }
        .highlight {
            color: #B51A2B;
            font-weight: bold;
            animation: fadeIn 2s ease-in-out;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            color: #A6A6A6;
            font-size: 14px;
            animation: fadeIn 2s ease-in-out;
        }
        .logo {
            display: block;
            margin: 0 auto;
            width: 200px;
            height: 200px;
            animation: fadeIn 3s ease-in-out;
            animation: pulse 2s infinite;
        }
        @keyframes fadeIn {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }
        @keyframes pulse {
            0% {box-shadow: 0 0 15px #6EC6FF;}
            50% {box-shadow: 0 0 30px #A879FF;}
            100% {box-shadow: 0 0 15px #6EC6FF;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Welcome Animation
    if "welcome_shown" not in st.session_state:
        with st.spinner("Loading AURA..."):
            time.sleep(2)  # Simulate loading time
        st.session_state.welcome_shown = True
        st.balloons()
        

    # Main Header
    st.markdown("<h1 class='main-title'>✨ AURA: Pembantu Pintar Pembelajaran Peribadi ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>Your personal smart assistant for time management and productivity</p>", unsafe_allow_html=True)

    # Animated Logo (Center)
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)

    lottie_aura = load_lottiefile("lottiefiles/aurarobot.json")

    col1, col2 = st.columns([0.8,1.5])

    with col2:
        st_lottie(lottie_aura, height=350, width=350, key="robot", quality="high",)

    with col1:
        st.markdown("")

    # Progress Indicator
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("### 🚀 Initializing Features...")
        progress_bar = st.progress(0)
        for percent in range(0, 101, 5):
            time.sleep(0.1)  # Simulate progress
            progress_bar.progress(percent)
    placeholder.empty()

    # Features Section
    st.markdown("### 🚀 Explore AURA's Features")

    col1, col2 = st.columns(2)

    # Feature 1
    with col1:
        st.markdown(
            """
            <div class='feature-box'>
                <h4>📅 Add Events to Calendar</h4>
                Effortlessly manage events by syncing with Google Calendar for a seamless experience.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Feature 2
    with col2:
        st.markdown(
            """
            <div class='feature-box'>
                <h4>😌 FaceID and Emotion Detection</h4>
                Detect your mood with real-time face recognition to personalize your experience.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Feature 3
    with col1:
        st.markdown(
            """
            <div class='feature-box'>
                <h4>📋 Schedule Maker</h4>
                Automatically generate personalized study schedules based on your upcoming exams and assignments.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Feature 4
    with col2:
        st.markdown(
            """
            <div class='feature-box'>
                <h4>💬 Chatbot</h4>
                Engage in personalized conversations that adapt to your preferences and provide helpful assistance.
            </div>
            """,
            unsafe_allow_html=True,
        )


    # Footer
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")

    st.sidebar.markdown(
        """
        <div class='footer'>
            © 2025 AURA. Designed for students, by students.
        </div>
        """,
        unsafe_allow_html=True,
    )

def chat_bot(username): #interface
    model = ai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction = (
            "You are AURA, an intelligent assistant dedicated to helping users excel in their studies, "
            "plan their schedules, and boost their productivity. Your role includes creating detailed study plans, "
            "managing event schedules, and offering personalized advice tailored to users' academic needs. "
            "Adapt your responses based on the user's input language. Follow these guidelines strictly:\n\n"
            "- **Language Flexibility:** Respond in Malay if the user's prompt is in Malay. Otherwise, respond in English.\n"
            "- **Student-Centric Focus:** Center all advice and suggestions around academic success, time management, and personal growth.\n"
            "- **Professional yet Casual:** Maintain a tone that is empathetic, understanding, and approachable, while staying professional.\n"
            "- **Clarity and Simplicity:** Use straightforward and easy-to-understand language, avoiding technical jargon unless requested.\n"
            "- **Halal and Ethical Practices:** Ensure all recommendations and suggestions adhere to halal and ethical standards.\n"
            "- **Actionable Guidance:** Provide clear, actionable, and specific suggestions tailored to the user's needs and context.\n\n"
            "Your ultimate goal is to be a friendly, supportive, and motivational academic companion who makes studying easier and more effective for the user."
        )
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_model" not in st.session_state:
        st.session_state.chat_model = model.start_chat(history=[])

    # Chat scrolling container
    st.markdown(
        """
        <style>
        .chat-container {
            max-height: 20px; /* Adjust as needed */
            overflow-y: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    unique_key = f"inputforprompt_{st.session_state.get('username', 'default')}"
    prompt = st.chat_input("Message AURA", key=unique_key)

    if prompt:
        st.chat_message("user").markdown(f"{username}: {prompt}")  # Print user input
        st.session_state.messages.append({"role": "user", "content": f"{username}: {prompt}"})  # Store user input in session state

        # Update chat history with the user's input
        st.session_state.chat_model.history.append({"role": "user", "parts": prompt})

        # Generate a response
        responses = st.session_state.chat_model.send_message(prompt)

        if responses and responses.candidates:
            assistant_reply = responses.candidates[0].content.parts[0].text  # Extract generated text
        else:
            assistant_reply = "Sorry, I couldn't process your request. Please try again."

        # Update the chat history with assistant's response
        st.session_state.chat_model.history.append({"role": "model", "parts": assistant_reply})

        # Display assistant's reply
        st.chat_message("assistant").markdown(f"Aura: {assistant_reply}")
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

        # jessay(assistant_reply)

def chatbot_input(prompt, username): #chatbot input
    model = ai.GenerativeModel(
        model_name="gemini-2.5-flash",
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

    chat = model.start_chat()
    respemo = chat.send_message(prompt)
    
    if respemo and respemo.candidates:
        respemobot = respemo.candidates[0].content.parts[0].text  # Extracts the generated text
    else:
        respemobot = "Sorry, I couldn't process your request. Please try again."
    
    return respemobot

def tell_date():
     # Tells Aura what's the date
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%A, %d %B %Y")
    formatted_time = current_datetime.strftime("%I:%M %p")
    st.session_state.chat_history.append({"role": "model", "parts": f"Today's date is {formatted_date}. The time is {formatted_time}"})

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
    now = datetime.now().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def ask_generative_ai_to_create_timetable(events):
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%A, %d %B %Y")
    formatted_time = current_datetime.strftime("%I:%M %p")

    """Send events to Google Generative AI to generate a study timetable."""
    ai.configure(api_key=GENAI_API_KEY)  # Replace with your actual API key

    model = ai.GenerativeModel(
        model_name="gemini-2.5-flash",
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

    Please create a study timetable around these events in a form of table, ensuring that I have at least 2 hours of study time per day. Focus on balancing study sessions and breaks.
    Today's date is {formatted_date}. The time is {formatted_time}
    """

    # Use Generative AI to process the prompt
    chat = model.start_chat()
    response = chat.send_message(prompt)
    
    if response and response.candidates:
        timetable = response.candidates[0].content.parts[0].text  # Extracts the generated text
    else:
        timetable = "Sorry, I couldn't process your request. Please try again."
    
    return timetable

def generatett():
    try:

        service = authenticate_user()
        events = fetch_calendar_events(service)

        # Send to Language Model and Display Timetable
        timetable = ask_generative_ai_to_create_timetable(events)

        st.write("Generated Study Timetable:")
        st.chat_message("assistant").markdown(timetable)

    except Exception as e:
        st.error(f"Error: {e}")

def startfeg(username):
    model = ai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=(
            "You are AURA, an intelligent assistant designed to help users manage their studies, "
            "plan schedules, and improve productivity. You provide polite, concise, and accurate "
            "responses. Your tasks include creating study timetables, offering real-time feedback based "
            "on user emotions, assisting with event scheduling, and offering personalized advice based on users' moods. " 
            "Use user-provided context to generate specific and actionable suggestions. Adhere strictly to these guidelines:\n"
            "- Focus on students and academic success.\n"
            "- Be empathetic, understanding, and professional but casual.\n"
            "- Ensure responses are simple and easy to understand, avoiding technical jargon unless necessary.\n"
            "- Prioritize halal and ethical practices in any recommendations.\n"
            "Your goal is to act as a dedicated and helpful academic companion."
        )
    )

    # Initialize chat model and history
    if "chat_model" not in st.session_state:
        st.session_state.chat_model = model.start_chat(history=[
            {"role": "user", "parts": f"My name is {username}."},
            {"role": "model", "parts": f"Hello {username}, it's great to see you! How can I assist you today?"},
        ])

    # Load the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_detected_time = None  # Tracks when a face is first detected
    face_stable_duration = 0.5  # Time in seconds to confirm a stable face detection
    detected_emotion = None  # Store the last detected emotion
    lottie_scanning = load_lottiefile("lottiefiles/facescan.json")

    # Load the enrolled face encoding
    try:
        known_face = np.load("user_face.npy")
    except FileNotFoundError:
        st.sidebar.error("No enrolled face found. Please register FaceID first.")
        return

    cap = cv2.VideoCapture(0)
    print("Waiting for the user.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

         # Convert frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Convert frame to RGB for emotion detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        # Draw rectangles around detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # If a face is detected
        if len(face_locations) > 0:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            match_results = face_recognition.compare_faces([known_face], face_encodings[0], tolerance=0.6)

            if match_results[0]:
                # Check if any faces were detected by Haar cascade
                if len(faces) > 0:
                    # The user is detected
                    if face_detected_time is None:
                        face_detected_time = time.time()  # Start the timer when the user detected

                    elapsed_time = time.time() - face_detected_time
                    print(f"{username} detected. Scanning for {elapsed_time:.1f} seconds...")

                    # If face detected continuously for the required duration
                    if elapsed_time >= face_stable_duration:
                        (x, y, w, h) = faces[0]  # Use the first detected face
                        face_roi = frame[y:y + h, x:x + w]

                        try:
                            # Analyze the face region for emotion
                            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                            detected_emotion = result[0]['dominant_emotion']

                            lottiescan()

                            # Greet the user
                            aurareply = greetwithemotion(detected_emotion, username)
                            st.chat_message("assistant").markdown(f"Aura: {aurareply}")
                            jessay(aurareply)              
                            print(f"Greeting sent: {aurareply}")

                            # Stop scanning and switch to chat mode
                            break
                        except Exception as e:
                            print(f"Error analyzing face: {e}")
                else:
                    print("No face detected by Haar cascade. Waiting...")
                    face_detected_time = None  # Reset detection timer
            else:
                print("Face not recognized. Try again.")
        else:
            # Reset if the face is not stable
            face_detected_time = None
            print("No face detected. Waiting...")

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)

    cap.release()
    cv2.destroyAllWindows()

def lottiescan ():
    lottie_scanning = load_lottiefile("lottiefiles/facescan.json")
    placeholder = st.empty()
    with placeholder.container():
        col1, col2 = st.columns([0.86,1.5])

        with col2:
            st.markdown(
                """
                <style>
                .lottie-container {
                    position: sticky;
                    text-align: center; /* Center it */
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Display the Lottie animation
            with st.container():
                st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
                st_lottie(lottie_scanning, speed=0.5, loop=False, height=300, width=300)
                time.sleep(2.6)
                st.markdown("</div>", unsafe_allow_html=True)

        with col1:
            st.markdown(
                """
                <div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    placeholder.empty()

def greetwithemotion(detected_emotion, username):
    model = ai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=(
            "You are AURA, a supportive and empathetic assistant designed to greet users and provide academic and emotional support. "
            "Your primary goals are to:\n"
            "- Greet the user briefly while acknowledging their emotional state.\n"
            "- Ask about their studies and offer assistance if needed.\n"
            "Guidelines for emotional responses:\n"
            "- If the user is happy or neutral, give positive reinforcement and maintain their good mood.\n"
            "- If the user is sad, offer uplifting words and motivate them.\n"
            "- If the user is angry, provide calming support.\n"
            "- If the user feels fear, reassure them with comforting words and optionally include a short Islamic quote.\n"
            "- If the user is surprised, acknowledge their surprise and offer brief assistance.\n"
            "- If the user feels disgust, empathize briefly and shift focus toward positivity.\n\n"
            "Other guidelines:\n"
            "- Keep responses short and simple, avoiding long explanations.\n"
            "- Always ask about their studies and offer specific help if possible.\n"
            "- Stay empathetic, professional, and culturally appropriate."
        )
    )

    chat = model.start_chat()

    # Dynamic prompt for greeting and academic follow-up
    prompt = (
        f"Greet the user named {username} briefly based on their emotional state ({detected_emotion}). "
        f"After greeting, ask about their studies and offer help if they need assistance. Keep it concise and empathetic."
        "Speak in Malay"
    )

    # Send the prompt to the model and get the response
    respemo = chat.send_message(prompt)

    if respemo and respemo.candidates:
        respemobot = respemo.candidates[0].content.parts[0].text.strip()  # Extract and clean up the generated text
    else:
        respemobot = (
            f"Hi {username}, I'm here to help! Let me know how your studies are going and how I can assist."
        )

    return respemobot
