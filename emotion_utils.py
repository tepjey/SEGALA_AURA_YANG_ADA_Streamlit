import cv2
from deepface import DeepFace
import streamlit as st
import time
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av

class EmotionDetector(VideoTransformerBase):
    def __init__(self):
        # Load the cascade classifier inside the class
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.last_emotion = "Neutral"

    def transform(self, frame):
        # Convert the frame (av.VideoFrame) to a numpy array (cv2 image)
        img = frame.to_ndarray(format="bgr24")
        gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = img[y:y + h, x:x + w]
            try:
                # Analyze the emotion (silent=True prevents console spam)
                result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False, silent=True)
                self.last_emotion = result[0]['dominant_emotion']

                # Draw rectangle and label
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, self.last_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            except Exception:
                # Fallback if DeepFace fails to analyze a face
                cv2.putText(img, "No face found", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Return the processed frame
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# New function to display the Streamlit component
def start_emotion_detection_web():
    # Use session state to store the result of the detection
    if 'detected_emotion' not in st.session_state:
        st.session_state.detected_emotion = "Neutral"

    # webrtc_streamer starts the camera and runs the EmotionDetector transformer
    ctx = webrtc_streamer(
        key="emotion-detection-key",
        video_processor_factory=EmotionDetector,
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        }
    )

    # Display the current emotion detected below the video stream
    if ctx.video_processor:
        st.session_state.detected_emotion = ctx.video_processor.last_emotion
        st.subheader(f"Current Emotion: {st.session_state.detected_emotion}")
        display_emotion_feedback(st.session_state.detected_emotion)
    else:
        st.write("Click 'Start' above to begin emotion detection.")

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