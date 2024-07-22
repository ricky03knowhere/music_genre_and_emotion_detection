import pandas as pd
import altair as alt
import time
from tensorflow.keras.models import load_model
from utils.mfcc_extractor import *
from utils.utils import *

genres = {
    "Blues": 0,
    "Classical": 0,
    "Country": 0,
    "Disco": 0,
    "HipHop": 0,
    "Jazz": 0,
    "Metal": 0,
    "Pop": 0,
    "Reggae": 0,
    "Rock": 0,
}
genres_list = list(genres.keys())
genre_detection_result = None


def model_service(model_path):
    st.write("Loading model... 🔃.")
    model = load_model(model_path)

    st.write("Extract MFCC... ✨.")

    if model_path == "./models/cnn__genre_detection_44100hz_0.91.h5":
        val = extract_mfcc(file_path="scipy.wav")
        val = np.array(val)
        val = val[..., np.newaxis]
    else:
        val = load_and_preprocess_data(file_path="scipy.wav")

    data = pd.DataFrame({"genres": genres_list, "values": list(genres.values())})
    st.write("Prediction starting... 🚀")
    prediction = model.predict(val)

    for i in range(prediction.shape[0]):
        for idx, v in enumerate(prediction[i]):
            # genres[genres_list[idx]] = genres[genres_list[idx]] + v
            genres[genres_list[idx]] = ((genres[genres_list[idx]] * 3) + v) / 4


def model_result():
    st.write("<<========= Genre Detection Accuracy =======>>")
    # Sort the two lists together based on values in descending order
    global genres
    st.write(genres)
    genre_values = list(genres.values())
    st.write(math.fsum(genre_values))
    sorted_genres = sorted(
        zip(genres_list, genre_values), key=lambda x: x[1], reverse=True
    )
    # st.write('sorted_genres ==> ', sorted_genres)
    global genre_detection_result
    for i, name in enumerate(genres_list):
        if name == sorted_genres[0][0]:
            st.write("genre detection result :", i)
            genre_detection_result = i
            break
    # Print the top 3 genres and their values
    val = 0
    for genre, value in sorted_genres[:3]:
        st.write("{}\t\t==> {}%".format(genre, round(value * 100, 2)))
        val += float(value)

    st.write(val)
    st.write(f"Others : {round((1  - val) * 100 , 2) }%")

    st.write("Prediction finished. 👌")


def get_genre_detection_result():
    global genre_detection_result
    return genre_detection_result
