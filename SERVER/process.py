import numpy as np
import tensorflow as tf
import numpy as np
from pathlib import Path

emotions = ['angry', 'anxious', 'apologetic', 'assertive', 'concerned', 'encouraging', 'excited', 'happy', 'neutral', 'sad']

def get_spectrogram(waveform):
    print(waveform)
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
    

    model = tf.keras.models.load_model(Path('model'))

    # print(model)
    from matplotlib import pyplot as plt
    im = plt.imshow(get_spectrogram(audioData))
    plt.show()
    prediction = model(get_spectrogram(audioData))
    return tf.nn.softmax(prediction[0])

print(interpretAudio(np.random.uniform(-1, 1, 44100)))