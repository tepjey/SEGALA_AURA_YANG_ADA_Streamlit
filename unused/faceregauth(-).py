import json
import cv2
import numpy as np  # Correct import for NumPy
import face_recognition
import streamlit as st
import time
from deepface import DeepFace
from streamlit_lottie import st_lottie
from startwemo import greet_user

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def authenticate_user():
    # Load the enrolled face encoding
    try:
        known_face = np.load("user_face.npy")
    except FileNotFoundError:
        print("No enrolled face found. Please register a face first.")
        return

    cap = cv2.VideoCapture(0)
    print("Look into the camera to authenticate.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        # Draw rectangles around detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # If a face is detected
        if len(face_locations) > 0:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Compare the detected face with the known face
            match_results = face_recognition.compare_faces([known_face], face_encodings[0], tolerance=0.6)

            if match_results[0]:
                print("Authentication successful!")
                cv2.putText(frame, "Authentication Successful", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow("Face Authentication", frame)
                cv2.waitKey(2000)  # Display the success message for 2 seconds
                break
            else:
                print("Face not recognized. Try again.")
                cv2.putText(frame, "Face Not Recognized", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the video feed
        cv2.imshow("Face Authentication", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Authentication canceled.")
            break

    cap.release()
    cv2.destroyAllWindows()

def authenticate_user_and_emotion(username):
    # Load the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_detected_time = None  # Tracks when a face is first detected
    face_stable_duration = 2.5  # Time in seconds to confirm a stable face detection
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

        # Convert frame to RGB
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

                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

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
                        st.write(f"Hello, {username}!")
                        print(f"Emotion detected: {detected_emotion}")
                        # greet_user(detected_emotion)

                        # Stop scanning after detecting emotion
                        break
                    except Exception as e:
                        print(f"Error analyzing face: {e}")
            else:
                print("Face not recognized. Try again.")
        else:
            # Reset if the face is not stable
            face_detected_time = None
            print("No face detected. Waiting...")

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            st.sidebar.error("Aura Shut Down")
            break

        time.sleep(0.1)

    cap.release()