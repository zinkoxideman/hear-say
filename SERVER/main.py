from asyncio.windows_events import NULL
from gc import callbacks
from oocsi import OOCSI
import time
from numpy import matrix, dot
from process import interpretAudio



class Recordings():
    def __init__(self):
        self.chunks = {}

    def process(self, chunk, sender, marker):
        self.addChunk(chunk, sender)
        if marker:
            emotion = interpretAudio(self.chunks[sender])
            self.delRecord(sender)
            return emotion
        return NULL

    def addChunk(self, chunk, sender):
        if sender in self.chunks.keys:
            self.chunks[sender] += chunk
        else:
            self.chunks[sender] = chunk

    def delRecord(self, sender):
        self.chunks.pop(sender)

class Emotions():
    def __init__(self):
        self.database = []

    #emotion is a 10D vector that contains a value for each of the emotions in the following shape 
    #[angry, anxious, apologetic, assertive, concerned, encouraging, excited, happy, neutral, sad]
    def getColor(self, emotion):
        #the following matrix holds the color weights that contain the color per emotion
        weights = matrix(
            [[1, 0, 0],
            [0, 0, 1],
            [0, 0.5, 0.5],
            [0.8, 0, 0.2],
            [0, 0.3, 0.7],
            [0, 0.3, 0.7],
            [0, 0.3, 0.7],
            [0, 0.3, 0.7],
            [0, 0.3, 0.7],
            [0.33, 0.33, 0.33]]
        )
        return (dot(emotion, weights).tolist())[0]

    def add(self, emotion, author):
        #delete any previous emotions from this autor
        self.removeAuthor(author)

        entry = {}
        entry['timeStamp'] = time.time()
        entry['emotion'] = emotion
        entry['author'] = author
        self.database.append(entry)
        self.getBlend()

    #remove any outdated records
    def removeOutdated(self):
        currentTime = time.time()
        # keep only items that are younger than 1 hour (3600s)
        self.database = [entry for entry in self.database if (currentTime - entry['timeStamp']) < 3600]

    def removeAuthor(self, author):
        [entry for entry in self.database if entry['author'] != author]

    #get a time weighted average of the emotions in the database
    def getBlend(self):
        self.removeOutdated()
        emotions = [0]*10

        #loop over each entry of the past hour
        for entry in self.database:
            for i in range(len(emotions)):
                emotions[i] += (entry['emotion'])[i]
        
        #normalize the blended emotions
        self.blend =  [emotion/sum(emotions) for emotion in emotions]


def handleMessage(sender, recipient, event):
    print(sender, "-->", recipient)
    print('message contains', len(event['chunk']), 'samples')
    print('flag', event['flag'], '\n')
    recordingEmotion = recordings.process(event['chunk'], sender, event['flag'])
    if recordingEmotion: #check if all the chunks have been received
        emotions.add(recordingEmotion, sender)
        message = {}
        message['color'] = emotions.getColor(emotions.getBlend())
        oocsi.send('hearSayChannel', message)
        print(message)

#creating the emotion and recording objects
emotions = Emotions()
recordings = Recordings()

#initializing the oocsi connection
#change the following line to get a handle automatically
oocsi = OOCSI('hearSayServer', 'oocsi.id.tue.nl', callback=handleMessage)