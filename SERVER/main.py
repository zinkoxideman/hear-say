from oocsi import OOCSI
import time
from numpy import matrix, dot
from recognise import interpretAudio

#change the following line to get a handle automatically
oocsi = OOCSI('hearSayServer', 'oocsi.id.tue.nl')

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

    def add(self, emotion):
        entry = {}
        entry['timeStamp'] = time.time()
        entry['emotion'] = emotion
        self.database.append(entry)

    #remove any outdated records
    def removeOutdated(self):
        currentTime = time.time()
        # keep only items that are younger than 1 hour (3600s)
        self.database = [entry for entry in self.database if (currentTime - entry['timeStamp']) < 3600]

    #get a time weighted average of the emotions in the database
    def getBlend(self):
        self.removeOutdated()
        currentTime = time.time()
        emotions = [0]*10

        #loop over each entry of the past hour
        for entry in self.database:
            timeWeight = 3600 + entry['timeStamp'] - currentTime
            for i in range(len(emotions)):
                emotions[i] += ((entry['emotion'])[i])*timeWeight
        
        #normalize the blended emotions
        return [emotion/sum(emotions) for emotion in emotions]
    

emotion = Emotions()
emotion.add([0.8,0.2,0,0,0,0,0,0,0,0])
while True:
    if len(emotion.database) > 0:
        message = {}
        message['color'] = emotion.getColor(emotion.getBlend())
        oocsi.send('hearSayChannel', message)
        print(message)
        time.sleep(5)
    else:
        print("emotions stored in database at the moment")