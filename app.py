import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import math
from collections import deque
from gtts import gTTS
import tempfile
import base64   # penting untuk autoplay audio

# ==============================
# Hand Gesture Recognizer Class
# ==============================
class HandGestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.gesture_buffer = deque(maxlen=10)

    def calculate_distance(self, point1, point2):
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def is_finger_up(self, landmarks, tip, pip):
        return landmarks[tip].y < landmarks[pip].y

    def detect_gesture(self, landmarks):
        thumb_tip, thumb_ip = 4, 3
        index_tip, index_pip = 8, 6
        middle_tip, middle_pip = 12, 10
        ring_tip, ring_pip = 16, 14
        pinky_tip, pinky_pip = 20, 18

        fingers_up = [
            landmarks[thumb_tip].x > landmarks[thumb_ip].x,
            self.is_finger_up(landmarks, index_tip, index_pip),
            self.is_finger_up(landmarks, middle_tip, middle_pip),
            self.is_finger_up(landmarks, ring_tip, ring_pip),
            self.is_finger_up(landmarks, pinky_tip, pinky_pip),
        ]

        if self.calculate_distance(landmarks[thumb_tip], landmarks[index_tip]) < 0.05:
            return "pinch"
        elif fingers_up == [False, True, True, False, False]:
            return "peace"
        elif fingers_up == [False, False, True, False, False]:
            return "thumbs_up"
        elif (self.calculate_distance(landmarks[thumb_tip], landmarks[index_tip]) < 0.08 
              and fingers_up[2:] == [True, True, True]):
            return "ok_sign"
        elif not any(fingers_up[1:]):
            return "fist"
        return "none"

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        with self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        ) as hands:
            results = hands.process(frame_rgb)
            gesture = "none"
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style(),
                    )
                    gesture = self.detect_gesture(hand_landmarks.landmark)
            return gesture, frame

# ==============================
# TTS helper
# ==============================
def speak_gtts(text):
    tts = gTTS(text)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name

# ==============================
# Streamlit UI
# ==============================
st.title("✋ Hand Gesture Recognition (with Voice in Cloud)")
st.write("Ambil gambar tangan → sistem deteksi gesture → suara diputar otomatis 🎧")

recognizer = HandGestureRecognizer()
img_file = st.camera_input("📷 Ambil gambar tangan")

if img_file:
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)

    gesture, processed_frame = recognizer.process_frame(frame)

    st.image(processed_frame, channels="BGR", caption=f"Gesture: {gesture.upper()}")

    responses = {
        'pinch': "Love you!",
        'peace': "Peace and love!",
        'thumbs_up': "Fuck you, bitch!",
        'ok_sign': "OK! Everything's perfect!",
        'fist': "Power fist! Show your strength!",
        'none': "No gesture detected"
    }
    st.success(responses[gesture])

    # 🔊 Auto play sound with gTTS
    if gesture != "none":
        audio_file = speak_gtts(responses[gesture])
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
