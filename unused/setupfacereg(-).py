import json
import cv2
import face_recognition
import numpy as np
import time
import streamlit as st
from streamlit_lottie import st_lottie
from aura import jessay

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def enroll_user(username):
    cap = cv2.VideoCapture(0)
    st.write("Look straight at the camera for enrollment.")

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

            lottie_scanning = load_lottiefile("lottiefiles/facescan.json")
            placeholder = st.empty()
            with placeholder.container():
                st_lottie(lottie_scanning, speed=1.0, loop=False, height=200, width=200)
                time.sleep(2.5)
            placeholder.empty()

            np.save("user_face.npy", face_encoding)  # Save the encoding for later use
            break

        cv2.imshow("Enrollment", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            st.error("Setup canceled.")
            break

    cap.release()
    cv2.destroyAllWindows()