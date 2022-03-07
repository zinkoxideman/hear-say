import numpy as np
import tensorflow as tf
import numpy as np

emotions = ['angry', 'anxious', 'apologetic', 'assertive', 'concerned', 'encouraging', 'excited', 'happy', 'neutral', 'sad']

def get_spectrogram(waveform):
    # # Convert the waveform to a spectrogram via a STFT.
    spectrogram = tf.signal.stft(waveform, frame_length=255, frame_step=128)
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


def interpretAudio(audioData):
    print("hoi")

    model = tf.keras.models.load_model('C:/Users/20193530/OneDrive - TU Eindhoven/Desktop/New folder (2)/New folder/hear-say/SERVER/model/')

    # print(model)
    print(get_spectrogram(tf.squeeze(audioData, axis=-1)))
    prediction = model(get_spectrogram(tf.squeeze(audioData, axis=-1)))
    return tf.nn.softmax(prediction[0])

interpretAudio(np.random.rand(44100, 1))