import math
import librosa
import streamlit as st

SAMPLE_RATE = 44100
TRACK_DURATION = 30  # second
SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION


def extract_mfcc(file_path, num_mfcc=13, n_fft=2048, hop_length=512, num_segments=10):
    # dictionary to store mapping, labels, and MFCCs
    data = []
    print("num_segments ==>", num_segments)
    samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)

    signal, sample_rate = librosa.load(file_path, sr=SAMPLE_RATE)
    # signal = np.array(file_path)
    # print(signal)
    print('length ==>', signal.shape)

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


    for d in range(num_segments):
        # calculate start and finish sample for current segment
        start = samples_per_segment * d
        finish = start + samples_per_segment

        # extract mfcc
        mfcc = librosa.feature.mfcc(
            y=middle_audio[start:finish],
            sr=SAMPLE_RATE,
            n_mfcc=num_mfcc,
            n_fft=n_fft,
            hop_length=hop_length,
        )
        mfcc = mfcc.T

        # store only mfcc feature with expected number of vectors
        if len(mfcc) == num_mfcc_vectors_per_segment:
            data.append(mfcc.tolist())

    return data