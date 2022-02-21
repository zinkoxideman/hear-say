from machine import ADC, Pin
import time

class Microphone():
    def __init__(self, pin = 32):
        self.microphone = ADC(Pin(pin))
    
    #record one chunk of audio from the microphone
    def readChunk(self, chunkSize = 4096):
        #do the recording
        return audioChunk

class ldr():
    self.status = 0
    def __init__(self, pin = 5):
        self.pin = Pin(pin, Pin.IN)
    
    def checkStatus():
        #check if the jar has been lifted up
        if self.pin.value():
            return True
        return False