import os
import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
# Spotify Client
client = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
    ),
    # redirect_uri="localhost:8501",
)


# Song Searching
def search_song(emotion, genre_select, artist, year, song_result):
    st.html(
        '<h3 style="margin-top: 1.5em;color:lightSalmon">Music Recomendations 🪄✨</h3>'
    )

    result = {}
    # st.write("after ==>", genre_select)

    emotion_label = ["happy", "sad", "angry", "love", "neutral", "surprise"]
    genre_label = ["happy", "sad", "hardcore", "romance", "chill", "heavy-metal"]

    cornverter = {i: j for (i, j) in zip(emotion_label, genre_label)}

    emotion_idx = None
    if emotion:
        emotion_idx = cornverter[emotion]

    separator = "," if emotion_idx and genre_select else ""
    genre_select = genre_select if (genre_select is not None) else ""
    emotion_idx = emotion_idx if (emotion_idx is not None) else ""

    if year is not None:
        year = f"{year[0]}-{year[1]}"
    else:
        year = ""

    keyword = (
        f"genre={genre_select}{separator}{emotion_idx}&artist={artist}&year={year}"
    )
    st.write(keyword)
    # if genre_select is not None:
    try:
        result = client.search(q=keyword, type="track", limit=song_result)
        print("result ==>", result)
    except Exception as err:
        print(err)
    # elif emotion is not None:
    #     result = client.search(q=emotion, type="track", limit=3)
    # else:
    # st.warning('Please select the genre first!')

    # Get Tracks List
    # st.json(result and result)
    if result["tracks"]["items"]:
        tracks = []
        # st.json(result["tracks"]["items"])
        for track in result["tracks"]["items"]:
            tracks.append(
                {
                    "title": track["name"],
                    "href": track["external_urls"]["spotify"],
                    "artists": track["artists"],
                    "picture": track["album"]["images"][1]["url"],
                    "year": track["album"]["release_date"],
                    "preview_url": track["preview_url"],
                }
            )
        # st.json(tracks)

        rows = [
            st.columns([2, 3], vertical_alignment="center") for i in range(len(tracks))
        ]

        for idx, col in enumerate(rows):
            with col[0]:
                st.write(
                    f'<img src="{tracks[idx]["picture"]}" width="120" style="margin-left:8em;border-radius:120px"/>',
                    unsafe_allow_html=True,
                )
            with col[1]:
                st.write(
                    f'<h5 style="margin-top:2em"><a target="_blank" href="{tracks[idx]["href"]}" style="text-decoration:none;color: tomato">{tracks[idx]["title"]}</a></h5>',
                    unsafe_allow_html=True,
                )
                artists_name = [
                    f'<a target="_blank" href="{artist["external_urls"]["spotify"]}" style="text-decoration:none;color:gold">{artist["name"]}</a>'
                    for artist in tracks[idx]["artists"]
                ]

                st.write(
                    f'{" , ".join(artists_name)}<span style="margin:0 0.3em"> | </span> <span style="color:lightSalmon">{tracks[idx]["year"][:4]}</span>',
                    unsafe_allow_html=True,
                )

                if tracks[idx]["preview_url"]:
                    st.audio(tracks[idx]["preview_url"])
                else:
                    st.warning("⚠️ Preview is not available")
            idx += 1
    else:
        st.markdown("#### No song for recommendation ")
