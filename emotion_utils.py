import cv2
import time
from deepface import DeepFace
import streamlit as st

def detect_emotion():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    last_emotion = None
    last_record_time = time.time()  # Initialize the timer

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

                # Check if 1 second has passed since the last recording
                if time.time() - last_record_time >= 0.5:
                    last_emotion = current_emotion
                    last_record_time = time.time()  # Reset the timer

                # Draw rectangle and label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, current_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            except Exception as e:
                print(f"Error analyzing face: {e}")

        cv2.imshow('Real-time Emotion Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Return the last detected emotion
    return last_emotion

# Emotion-to-recommendation mapping
emotion_recommendations = {
    'happy': "Keep up the great work! Consider celebrating your achievements.",
    'sad': "Take a break and do something you enjoy. Reach out to a friend for support.",
    'angry': "Take deep breaths. A short walk or mindfulness exercise can help.",
    'fear': "Identify the source of your fear. Try grounding techniques to stay calm.",
    'surprise': "Reflect on the unexpected event. It might be an opportunity!",
    'neutral': "Maintain your focus and continue your tasks as planned.",
    'disgust': "Step away from what's causing discomfort and engage in something pleasant."
}

# Get recommendation based on emotion
def get_recommendation(emotion):
    return emotion_recommendations.get(emotion, "No recommendation available.")

def display_emotion_feedback(detected_emotion):
    st.write(f"### Detected Emotion: {detected_emotion}")
    recommendation = get_recommendation(detected_emotion)
    if detected_emotion in ['happy', 'neutral']:
        st.success(recommendation)
    elif detected_emotion in ['sad', 'fear', 'surprise']:
        st.warning(recommendation)
    elif detected_emotion in ['angry', 'disgust']:
        st.error(recommendation)