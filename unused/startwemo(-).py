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
    st.sidebar.success(f"Detected Emotion: {emotion}")
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

def startemotionface():
    # Load the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    face_detected_time = None  # Tracks when a face is first detected
    face_stable_duration = 1.5  # Time in seconds to confirm a stable face detection
    detected_emotion = None  # Store the last detected emotion
    lottie_scanning = load_lottiefile("lottiefiles/facescan.json")

    print("Face scanning started. Please look into the camera.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            # A face is detected
            if face_detected_time is None:
                face_detected_time = time.time()  # Start the timer when a face is first detected

            elapsed_time = time.time() - face_detected_time
            print(f"Face detected. Scanning for {elapsed_time:.1f} seconds...")

            # If face detected continuously for the required duration
            if elapsed_time >= face_stable_duration:
                (x, y, w, h) = faces[0]  # Use the first detected face
                face_roi = frame[y:y + h, x:x + w]

                try:
                    placeholder = st.empty()
                    with placeholder.container():
                        st_lottie(lottie_scanning, speed=0.1, loop=False, height=300, width=300)
                    placeholder.empty()

                    # Analyze the face region for emotion
                    result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                    detected_emotion = result[0]['dominant_emotion']
                    print(f"Emotion detected: {detected_emotion}")
                    greet_user(detected_emotion)

                    # Stop scanning after detecting emotion
                    break

                except Exception as e:
                    print(f"Error analyzing face: {e}")

        else:
            # Reset if the face is not stable
            face_detected_time = None
            print("No face detected. Waiting...")

        # Add a small delay to reduce CPU usage
        time.sleep(0.1)

    cap.release()