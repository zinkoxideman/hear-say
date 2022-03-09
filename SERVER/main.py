from asyncio.windows_events import NULL
from email.mime import audio
from gc import callbacks
from oocsi import OOCSI
import time
from numpy import matrix, dot
import numpy as np
import tensorflow as tf
from pathlib import Path
from matplotlib import pyplot as plt

emotions = ['angry', 'anxious', 'apologetic', 'assertive', 'concerned', 'encouraging', 'excited', 'happy', 'neutral', 'sad']

class Emotions():
    def __init__(self):
        self.database = []

    #emotion is a 10D vector that contains a value for each of the emotions in the following shape 
    #[angry, anxious, apologetic, assertive, concerned, encouraging, excited, happy, neutral, sad]
    def getColor(self, emotion):
        #the following matrix holds the color weights that contain the color per emotion
        weights = matrix(
            [[255, 0, 128],
            [255, 128, 0],
            [255, 0, 128],
            [128, 0, 255],
            [128, 0, 255],
            [128, 255, 128],
            [180, 255, 0],
            [255, 255, 0],
            [128, 255, 180],
            [0, 128, 255]]
        )
        colors =  (dot(emotion, weights).tolist())[0]
        return [int(value) for value in colors]

    def add(self, emotion, author):
        #delete any previous emotions from this autor
        self.removeAuthor(author)

        entry = {}
        entry['timeStamp'] = time.time()
        entry['emotion'] = emotion
        entry['author'] = author
        self.database.append(entry)

    #get a time weighted average of the emotions in the database
    def getBlend(self):
        self.removeOutdated()
        print("removed any and all outdated emotions")
        emotion_sum = [0]*10

        #loop over each entry of the past hour
        for entry in self.database:
            for i in range(len(emotion_sum)):
                emotion_sum[i] += (entry['emotion'])[i]
        
        #normalize the blended emotions
        self.blend =  [emotion/sum(emotion_sum) for emotion in emotions]
    
    #remove any outdated records
    def removeOutdated(self):
        currentTime = time.time()
        # keep only items that are younger than 1 hour (3600s)
        self.database = [entry for entry in self.database if (currentTime - entry['timeStamp']) < 3600]

    def removeAuthor(self, author):
        [entry for entry in self.database if entry['author'] != author]
    
#creating the emotion object
emotions = Emotions()

class Recordings():
    def __init__(self):
        self.chunks = {}
        self.model = tf.keras.models.load_model(Path('model'))
        print(self.model)

    def process(self, chunk, sender, marker, oocsi):
        self.addChunk(chunk, sender)

        if marker == True:
            emotion = self.interpretAudio(self.chunks[sender])
            self.chunks[sender] = []
            emotions.add(emotion, sender)
            print('emotions: ', emotions.database)
            message = {}
            color = emotions.getColor(emotion)
            print("average color:",color)
            message['color'] = color
            oocsi.send('hearSayChannel', message)
            print(message)

    def addChunk(self, chunk, sender):
        if sender in self.chunks:
            self.chunks[sender] += chunk
        else:
            self.chunks[sender] = chunk
        return NULL

    def interpretAudio(self, audioData):
        print('test1')
        audioData = np.asarray(audioData)/2048.0 - np.ones(len(audioData))
        audioData = audioData - np.average(audioData)
        audioData = audioData/np.max(abs(audioData))
        print("audio data:",audioData)
        print("number of samples in set: ", len(audioData))
        print("printing the model:", self.model)
        
        spectrogram = tf.signal.stft(audioData, frame_length=255, frame_step=128)
        spectrogram = tf.abs(spectrogram)
        spectrogram = spectrogram[..., tf.newaxis]
        # resize the spectrogram so different length recordings are equal in size
        spectrogram = tf.image.resize(
            spectrogram, 
            [256, 256]
        )

        # im = plt.imshow(spectrogram)
        # plt.show()
        prediction = self.model(spectrogram)
        prediction =  tf.nn.softmax(prediction[0]).numpy().tolist()
        print("model prediction:", prediction)
        return prediction

# creating the recordings object
recordings = Recordings()

def handleMessage(sender, recipient, event):
    print("\n", sender, "-->", recipient)
    print('message contains', len(event['chunk']), 'samples')
    print('flag', event['flag'])
    recordings.process(event['chunk'], sender, event['flag'], oocsi)
        

#initializing the oocsi connection
#change the following line to get a handle automatically
oocsi = OOCSI('hearSayServer', 'oocsi.id.tue.nl', callback=handleMessage)