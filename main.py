import streamlit as st
import soundfile as sf
import io

from utils.mfcc_extractor import *
from utils.utils import *
from services.api_services import *
from services.audio_services import *
from services.model_services import *
from services.camera_services import *

st.title("Music Recommendation with Genre & Emotion Detection (production)")


st.html('<h3 style="margin-top: 1.5em;color:khaki">Song Parameters 🧪</h3')
artist = st.text_input("Artist name")

add_year = st.toggle("Insert year.?", value=True)

if add_year:
    year = st.slider("Song Release", 1980, 2024, [2016, 2020])
else:
    year = None

song_result = st.slider("Song result", 3, 20)


st.html('<h3 style="margin-top: 1.5em;color:khaki">Genre Detection 🎧</h3')
activate_genre = st.toggle("Activate Genre Detection")

if activate_genre:
    model_path = st.radio(
        "Select the model",
        [
            "./models/cnn__genre_detection_44100hz_0.91.h5",
            "./models/cnn__genre_detection_41100hz_0.95(Tripathi Dataset).h5",
        ],
        captions=["Model accuracy: 91%", "Model accuracy: 95% (Tripathi Dataset)"],
    )

    music_input_method = st.radio(
        "Select the method of music input",
        ["Record music 🎙️", "Upload music file 🎵"],
        captions=[
            "Record music sample around you",
            "Upload sample music from your device",
        ],
    )

    if music_input_method == "Record music 🎙️":
        # duration = st.slider("Select recording duration (seconds)", 0, 30, 30, 5)
        recording_btn = st.button("Start Recording ⏺️")
        if recording_btn:
            recoding_audio(30)
            model_service(model_path)
            model_result()

    else:
        uploaded_file = st.file_uploader("Upload Audio File", type=["wav", "mp3"])
        if uploaded_file is not None:
            audio_data = uploaded_file.getvalue()
            data, samplerate = sf.read(io.BytesIO(audio_data))
            sf.write("scipy.wav", data, samplerate)
            model_service(model_path)
            model_result()

    st.write("result", get_genre_detection_result())
    genre_select = st.selectbox(
        "Music genre to search",
        [
            "blues",
            "classical",
            "country",
            "disco",
            "hip-hop",
            "jazz",
            "metal",
            "pop",
            "reggae",
            "rock",
        ],
        index=get_genre_detection_result(),
    )
    st.write("before ==>", genre_select)


st.html('<h3 style="margin-top: 1.5em;color:khaki">Emotion Detection 🫠</h3')
activate_emotion = st.toggle("Activate Emotion Detection")

if activate_emotion:
    if "is_open" not in st.session_state:
        st.session_state["is_open"] = False

    detect_emotion = st.toggle("Open Camera 📸", value=st.session_state["is_open"])
    if detect_emotion:
        st.session_state["is_open"] = True
        np.save("./utils/emotion.npy", np.array([""]))
        st.write("is open :", detect_emotion)
        camera_service()

    st.session_state["is_open"] = False

    if st.session_state["is_open"] == False:
        st.session_state["run"] = "false"

    st.write("is open :", detect_emotion)
    st.write("is open state :", st.session_state["is_open"])
    st.write("in main :", get_emotion())
    emotion_label = ["happy", "sad", "angry", "love", "neutral", "surprise"]
    cornverter = {j: i for i, j in enumerate(emotion_label)}

    emotion_idx = None
    if get_emotion():
        emotion_idx = cornverter[get_emotion()]

    emotion = st.selectbox(
        "Pick one the emotion you feel now",
        ["happy", "sad", "angry", "love", "neutral", "surprise"],
        index=emotion_idx,
    )

    st.write("emotion ==>", emotion)
button_search = st.button("Search Song")
if button_search:
    st.session_state["run"] = "false"
    search_song(emotion, genre_select, artist, year, song_result)
