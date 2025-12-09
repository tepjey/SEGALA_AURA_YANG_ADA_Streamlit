import cv2
import time
from deepface import DeepFace
import pyttsx3
import json
import streamlit as st
from streamlit_lottie import st_lottie
import os
from dotenv import load_dotenv
from elevenlabs import Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs

load_dotenv()
client = ElevenLabs(
api_key=os.getenv("ELEVENLABS_KEY"),
)

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def analyze_emotion(frame, face_cascade):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        face_roi = frame[y:y + h, x:x + w]
        try:
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
            return result[0]['dominant_emotion']
        except Exception as e:
            st.error(f"Error analyzing emotion: {e}")
    return None

def greet_user(emotion):

    emotion_recommendations = {
        'happy': "Hello there! You seem happy today. Keep spreading positivity!",
        'sad': "You look a bit sad. Remember, tough times don’t last forever.",
        'angry': "Take a deep breath. Anger can be a stepping stone to calmness.",
        'fear': "It's okay to feel afraid. Focus on your strengths and keep going!",
        'surprise': "Wow! You seem surprised. I hope it’s something wonderful!",
        'neutral': "You’re looking calm. Ready to focus and achieve great things?",
        'disgust': "Let’s shake off that feeling and focus on something positive."
    }

    # Get the appropriate greeting or use a default one
    greeting = emotion_recommendations.get(emotion, "Hello there! Let's have a productive session.")
    
    # Display the greeting in Streamlit
    st.success(f"Detected Emotion: {emotion}")
    st.write(f"### AURA: {greeting}")

    try:
        audio = client.generate(
            text=greeting,
            voice=Voice(
                voice_id='cgSgspJ2msm6clMCkdW9',
                settings=VoiceSettings(stability=0.5, similarity_boost=0.5, style=1.0, use_speaker_boost=True)
            )
        )
        # play(audio)

    except Exception as e:
        st.error(f"An error occurred while generating or playing audio: {e}")

# Main Streamlit app
def app():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    lottie_scanning = load_lottiefile("lottiefiles/facescan.json")

    placeholder = st.empty()
    with placeholder.container():
        st_lottie(lottie_scanning, speed=0.1, loop=False, height=300, width=300)
        st.text("Detecting emotion... Please sit in front of the camera.")
        start_time = time.time()
        detected_emotion = None
        face_found = False

        while time.time() - start_time < 3:  # Run detection for 3 seconds
            ret, frame = cap.read()
            if not ret:
                st.error("Unable to access the webcam.")
                break
            
            emotion = analyze_emotion(frame, face_cascade)
            if emotion:
                detected_emotion = emotion  # Store the most recent detected emotion
                face_found = True
    placeholder.empty()

    cap.release()
    cv2.destroyAllWindows()

    if face_found:
        greet_user(detected_emotion)
    else:
        st.warning("No face detected. Please make sure you're sitting in front of the camera.")