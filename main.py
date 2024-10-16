import streamlit as st
import soundfile as sf
import io
import os

from utils.mfcc_extractor import *
from utils.utils import *
from services.api_services import *
from services.audio_services import *
from services.model_services import *
from services.camera_services import *


st.set_page_config(page_title="GenMotion", page_icon="icon.png")

st.title("Music Recommendation with Genre & Emotion Detection (production)")


st.html('<h3 style="margin-top: 1.5em;color:khaki">Song Parameters 🧪</h3')

with st.expander("Add Parameters"):
    artist = st.text_input("Artist name")

    add_year = st.toggle("Insert year.?", value=True)

    if add_year:
        year = st.slider("Song Release", 1980, 2024, [2016, 2020])
    else:
        year = None

    song_result = st.slider("Song result", 3, 20)

(
    tab1,
    tab2,
) = st.tabs(["Genre Detection 🎧", "Emotion Detection 🫠"])

with tab1:
    st.html('<h3 style="margin-top: .6em;color:khaki">Genre Detection 🎧</h3')

    model_path = "./models/cnn__genre_detection_41100hz_0.95(Tripathi Dataset).h5"

    music_input_method = st.radio(
        "Select the method of music input",
        ["Upload music file 🎵", "Record music 🎙️"],
        captions=[
            "Upload sample music from your device",
            "Record music sample around you",
        ],
    )

    if music_input_method == "Record music 🎙️":
        recording_btn = st.button("Start Recording ⏺️")
        if recording_btn:
            recoding_audio(30)
            model_service(model_path)
            model_result()
            search_song(get_genre_detection_result(), artist, year, song_result)

    else:
        uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])
        if uploaded_file is not None:
            audio_data = uploaded_file.getvalue()
            data, samplerate = sf.read(io.BytesIO(audio_data))
            sf.write("scipy.wav", data, samplerate)
            model_service(model_path)
            model_result()
            search_song(get_genre_detection_result(), artist, year, song_result)
            st.snow()

with tab2:
    st.html('<h3 style="margin-top: .6em;color:khaki">Emotion Detection 🫠</h3')

    if "is_open" not in st.session_state:
        st.session_state["is_open"] = False

    detect_emotion = st.toggle("Open Camera 📸", value=st.session_state["is_open"])
    if detect_emotion:
        st.session_state["is_open"] = True
        np.save("./utils/emotion.npy", np.array([""]))
        camera_service()

        st.session_state["is_open"] = False

        if st.session_state["is_open"] == False:
            st.session_state["run"] = "false"

        st.write("Emotion detection result :", get_emotion())

        if os.path.exists("/utils/emotion.npy"):
            os.remove("utils/emotion.npy")

        if st.button("Rerun Emotion Detection") :
            st.session_state["is_open"] = False
            st.rerun()
            
        search_song("", artist, year, song_result, emotion=get_emotion())