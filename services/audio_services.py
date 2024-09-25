import streamlit as st
import sounddevice as sd
import numpy as np
import time
import os
from utils.utils import save_audio

sample_rate = 44100  # samples per second
# sample_rate = 22050  # samples per second
buffer_size = 1024  # buffer size for real-time plotting

#  Define a callback function to collect audio data
recording = np.zeros(0)


def callback(indata, frames, time, status):
    global recording
    recording = np.append(recording, indata[:, 0])


def recoding_audio(duration):
    global recording

    st.write("Recording...")
    # duration_timer(duration)

    # Create an input stream with the callback
    stream = sd.InputStream(
        callback=callback, channels=1, samplerate=sample_rate, blocksize=buffer_size
    )
    stream.start()

    fig = st.bar_chart()
    # Update plot dynamically
    start_time = time.time()
    while time.time() - start_time < duration:
        if len(recording) > 0:
            fig.add_rows(
                recording[-duration:]
            )  # Plot the most recent 'duration' seconds of audio
        time.sleep(0.5)  # Update every 100 ms

    stream.stop()
    stream.close()
    st.write("Recording finished.")

    os.remove("scipy.wav")
    save_audio("scipy.wav", sample_rate, recording)
    recording = np.zeros(0)
