import os
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras import models
from IPython import display

from tkinter import Tk
from tkinter.filedialog import askopenfilename

emotions = ['angry', 'anxious', 'apologetic', 'assertive', 'concerned', 'encouraging', 'excited', 'happy', 'neutral', 'sad']

def decode_audio(file_path):    
    audio_binary = tf.io.read_file(file_path)
    # Decode WAV-encoded audio files to `float32` tensors, normalized
    # to the [-1.0, 1.0] range. Return `float32` audio and a sample rate.
    audio, _ = tf.audio.decode_wav(contents=audio_binary)
    # Since all the data is single channel (mono), drop the `channels`
    # axis from the array.
    return tf.squeeze(audio, axis=-1)


def get_spectrogram(waveform):
    # # Convert the waveform to a spectrogram via a STFT.
    spectrogram = tf.signal.stft(
        waveform, frame_length=255, frame_step=128)
    # Obtain the magnitude of the STFT.
    spectrogram = tf.abs(spectrogram)
    # Add a `channels` dimension, so that the spectrogram can be used
    # as image-like input data with convolution layers (which expect
    # shape (`batch_size`, `height`, `width`, `channels`).
    spectrogram = spectrogram[..., tf.newaxis]

    #resize the spectrogram so different length recordings are equal in size
    spectrogram = tf.image.resize(
        spectrogram, 
        [256, 256]
    )

    return spectrogram 

def interpretAudio():
    sample_file = 'J A Z Z.wav'

    model = tf.keras.models.load_model('model')

    prediction = model(get_spectrogram(decode_audio(sample_file)))
    tf.nn.softmax(prediction[0])