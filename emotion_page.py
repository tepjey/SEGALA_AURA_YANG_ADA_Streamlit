import cv2
import time
from deepface import DeepFace
import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as ai
from aura import jessay

def chat_bot_emotion(prompt):
    load_dotenv()
    GENAI_API_KEY = os.getenv("GENAI_API_KEY")

    if not GENAI_API_KEY:
        raise ValueError("API Key not found! Please set GOOGLE_GENAI_API_KEY.")

    ai.configure(api_key=GENAI_API_KEY)

    model = ai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        system_instruction = (
                            "Your name is AURA, an intelligent and supportive assistant designed to help users manage their emotions and provide encouragement. "
                            "You are assigned to respond based on the user's emotions, which can include happy, sad, angry, fear, surprise, neutral, or disgust. "
                            "Always state the user's detected emotion first before assisting them. Keep your responses short, simple, and supportive. "

                            "Here are the specific guidelines for each emotion:\n"
                            "- If the user is happy or neutral, praise them and provide positive reinforcement to maintain their good mood.\n"
                            "- If the user is sad, encourage them with uplifting words and motivate them to feel better.\n"
                            "- If the user is angry, calmly help them cool down and provide tips for managing anger effectively.\n"
                            "- If the user feels fear, reassure them that everything will be okay and include an Islamic quote to comfort them.\n"
                            "- If the user is surprised, ask them what happened and offer assistance where needed.\n"
                            "- If the user feels disgust, empathize with their feelings and shift the focus toward positivity and support.\n\n"

                            "Adhere strictly to these guidelines:\n"
                            "- Be empathetic, understanding, and professional in all responses.\n"
                            "- Ensure responses are easy to understand, avoiding technical jargon unless necessary.\n"
                            "- Prioritize halal and ethical practices in every recommendation.\n"
                            "- Keep discussions focused on emotional support and avoid speculative or unnecessary topics.\n"

                            "Your primary goal is to act as a kind, understanding, and motivational companion for the user. Respond in Bahasa Melayu pasar"
                        )
                    )


    if prompt:

        chat = model.start_chat()
        responses = chat.send_message(prompt)

        if responses and responses.candidates:
            assistant_reply = responses.candidates[0].content.parts[0].text  # Extracts the generated text
        else:
            assistant_reply = "Sorry, I couldn't process your request. Please try again."


        st.chat_message("assistant").markdown(assistant_reply)
        jessay(assistant_reply)

def detect_emotion():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    last_emotion = None
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]

            try:
                result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                current_emotion = result[0]['dominant_emotion']

                last_emotion = current_emotion

                # Draw rectangle and label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, current_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            except Exception as e:
                print(f"Error analyzing face: {e}")

        cv2.imshow('Real-time Emotion Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or time.time() - start_time > 5:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Return the last detected emotion
    return last_emotion

def display_emotion_feedback(emotion):
    if emotion is None:
        st.warning("There's problem occur") 
    else:
        prompt = f"user emotion is {emotion}"
        chat_bot_emotion(prompt)

def detect_emotion_pro():
    # Load the Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    last_emotion = None
    start_time = time.time()

    # Create a named OpenCV window and make it topmost
    window_name = "Real-time Emotion Detection"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]

            try:
                # Analyze the face region for emotion detection
                result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                current_emotion = result[0]['dominant_emotion']

                last_emotion = current_emotion

                # Draw rectangle and label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, current_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            except Exception as e:
                print(f"Error analyzing face: {e}")

        # Display the frame with detections
        cv2.imshow(window_name, frame)

        # Exit after 5 seconds or when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q') or time.time() - start_time > 5:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Return the last detected emotion
    return last_emotion