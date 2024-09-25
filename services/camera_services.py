import streamlit as st
import numpy as np
import time
from streamlit_webrtc import webrtc_streamer
from utils.emotion_detector import EmotionDetector

emotion = None


def camera_service():
    global emotion
    if "run" not in st.session_state:
        st.session_state["run"] = "true"

    try:
        emotion = np.load("./utils/emotion.npy")[0]
    except:
        emotion = ""

    if not (emotion):
        st.session_state["run"] = "true"
    else:
        st.session_state["run"] = "false"

    if st.session_state["run"] != "false":
        start_time = 0
        webrtc_streamer(
            key="key",
            desired_playing_state=True,
            video_processor_factory=EmotionDetector,
            sendback_audio=False,
        )

        st.info('Please wait...')
        while True:
            # with st.empty():
            if start_time >= 3:
                st.session_state["run"] = "false"
                break
            start_time += 1
            time.sleep(1)

    if not (emotion):
        st.info("Detecting your emotion state...")
        st.session_state["run"] = "true"
    else:
        # st.write(emotion)
        np.save("./utils/emotion.npy", np.array([""]))
        st.session_state["run"] = "false"


def get_emotion():
    try:
        emotion = np.load("./utils/emotion.npy")[0]
    except:
        emotion = ""
    return emotion
