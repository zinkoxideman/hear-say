from machine import Pin
import numpy as np

class Light():
    def __init__(self, pins = [16,17,18]): #set the default pins for the RGB light
        self.redChannel = Pin(pins[0], Pin.OUT)
        self.greenChannel = Pin(pins[1], Pin.OUT)
        self.blueChannel = Pin(pins[2], Pin.OUT)

    #emotion is a 10D vector that contains a value for each of the emotions in the following shape 
    #[angry, anxious, apologetic, assertive, concerned, encouraging, excited, happy, neutral, sad]
    def getColor(self, emotion):
        #the following matrix holds the color weights that contain the color per emotion
        weights = np.matrix(
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
        self.color = np.dot(emotion, weights)

    def applyColor(self):
        self.redChannel.value(self.color[0])
        self.greenChannel.value(self.color[1])
        self.blueChannel.value(self.color[2])

class Buzzer():
    self.frequency = 400
    def __init__(self, pin):
        self.pin = pin

    def confirm():
        #play a specific rythm to indicate recording has finished

    def received():
        #play a specific rythm to alert the user of a new message

    def startRec():
        #play a specific rythm to indicate that recording has started

    def sent():
        #play a specific rythm when the message was sent succesfully