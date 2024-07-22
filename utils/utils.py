import numpy as np
import librosa
import scipy.io.wavfile as wav
import streamlit as st
from tensorflow.image import resize


def save_audio(filename, sample_rate, data):
    max_val = np.max(np.abs(data))
    if max_val > 0:
        data = data / max_val

    wav.write(filename, sample_rate, (data * 32767).astype(np.int16))


# Load and preprocess audio data
def load_and_preprocess_data(file_path, target_shape=(150, 150)):
    data = []
    signal, sample_rate = librosa.load(file_path, sr=None)
    # audio_data = np.array(file_path)
    # sample_rate = 44100
    # Perform preprocessing (e.g., convert to Mel spectrogram and resize)
    # Define the duration of each chunk and overlap
    duration = len(signal) / sample_rate

    # Determine the start and end points for the middle 30 seconds
    start_time = (duration - 30) / 2
    end_time = start_time + 30

    # Convert time to sample indices
    start_sample = int(start_time * sample_rate)
    end_sample = int(end_time * sample_rate)

    # Extract the middle 30 seconds of audio
    middle_audio = signal[start_sample:end_sample]
    st.audio(middle_audio, format="audio/mpeg", sample_rate=sample_rate)

    chunk_duration = 4  # seconds
    overlap_duration = 2  # seconds

    # Convert durations to samples
    chunk_samples = chunk_duration * sample_rate
    overlap_samples = overlap_duration * sample_rate

    # Calculate the number of chunks
    num_chunks = (
        int(
            np.ceil(
                (len(middle_audio) - chunk_samples) / (chunk_samples - overlap_samples)
            )
        )
        + 1
    )

    # Iterate over each chunk
    for i in range(num_chunks):
        # Calculate start and end indices of the chunk
        start = i * (chunk_samples - overlap_samples)
        end = start + chunk_samples

        # Extract the chunk of audio
        chunk = middle_audio[start:end]

        # Compute the Mel spectrogram for the chunk
        mel_spectrogram = librosa.feature.melspectrogram(y=chunk, sr=sample_rate)

        # mel_spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate)
        mel_spectrogram = resize(np.expand_dims(mel_spectrogram, axis=-1), target_shape)
        data.append(mel_spectrogram)

    return np.array(data)
