
import streamlit as st
import json
import os
import cv2
import numpy as np
import time
import face_recognition
from streamlit_lottie import st_lottie
from aura import jessay

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

default_animation = load_lottiefile("lottiefiles/faceidlogo.json")  # Default looping animation
face_scanning_animation = load_lottiefile("lottiefiles/facescan.json")  # Face-scanning animation

def mainfaceid():
    
    # CSS for Custom Styling
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 40px;
            color: #FFA586;
            text-align: center;
        }
        .tagline {
            text-align: center;
            color: #A6A6A6;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )   

    # Main Header
    st.markdown("<h1 class='main-title'>Welcome to AURA's FaceID Setup! 😊</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>This step helps AURA recognize you and provide a personalized experience every time you log in.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,1.44])

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

        st_lottie(default_animation, speed=1.0, loop=True, height=250, width=250)

    with col1:
        st.markdown(
            """
            <div>
                <h1></h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Reset FaceID button in the sidebar
    if os.path.exists("user_face.npy"):
        button = st.sidebar.button("Reset FaceID", key="reset")
        if button:
            os.remove("user_face.npy")
            st.success("FaceID Successfully Reset")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("**Step 1:** Enter your nickname below 👇")
    st.session_state.username = st.text_input("What should AURA call you?", value=st.session_state.username, )

    st.markdown("**Step 2:** Click **Start** to begin setting up FaceID! 🎥")
    startsetup = st.button("Start Setup", key="startsetupfaceid")
    if startsetup:
        if st.session_state.username.strip():
            enroll_user(st.session_state.username)
            st.success(f"FaceID Setup Completed 🎉! AURA is ready to recognize you, {st.session_state.username}!")
            jessay(f"FaceID Setup Completed! AURA is ready to recognize you, {st.session_state.username}!")
        else:
            st.error("⚠️ Please enter your nickname before starting!")

def enroll_user(username):
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture frame.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        if len(face_locations) > 0:
            # Take the first face detected
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Display the frame
            cv2.imshow("Enrollment", frame)

            # Extract the face encoding
            face_encoding = face_recognition.face_encodings(rgb_frame, [face_locations[0]])[0]

            placeholder = st.empty()
            with placeholder.container():
                st.markdown("### Setting up FaceID...")
                progress_bar = st.progress(0)
            for percent_complete in range(101):
                time.sleep(0.02)  # Simulate progress
                progress_bar.progress(percent_complete)
            placeholder.empty()

            np.save("user_face.npy", face_encoding)  # Save the encoding for later use
            break

        cv2.imshow("Enrollment", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            st.error("Setup canceled.")
            break

    cap.release()
    cv2.destroyAllWindows()