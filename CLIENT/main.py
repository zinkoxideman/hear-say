from oocsi import OOCSI
from machine import ADC, Pin, PWM
from time import sleep_ms, sleep
from network import WLAN, STA_IF

# connect to the WIFI
wlan = WLAN(STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.scan()             # scan for access points
if not wlan.isconnected():
    wlan.connect('FRITZ!Box 7490', '26958267051151616039') # connect to an AP
    wlan.config('mac')      # get the interface's MAC address
    wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

class Light():
    def __init__(self, pins = [16,17,18]): #set the default pins for the RGB light
        self.redChannel = Pin(pins[0], Pin.OUT)
        self.greenChannel = Pin(pins[1], Pin.OUT)
        self.blueChannel = Pin(pins[2], Pin.OUT)

    def applyColor(self, color = [0,0,0]):
        self.redChannel.value(color[0])
        self.greenChannel.value(color[1])
        self.blueChannel.value(color[2])

class Buzzer():
    def __init__(self, pin=15, volume = 256):
        self.pin = Pin(pin, Pin.OUT)
        self.volume = volume
        
    def play_received(self):
        #play a specific rythm to alert the user of a new message
        buzzerPin = PWM(self.pin)
        buzzerPin.duty(self.volume)

        buzzerPin.freq(300)
        sleep_ms(500)
        buzzerPin.freq
        sleep_ms(400)

        buzzerPin.duty(0)
        buzzerPin.deinit()

    # def startRec(self):
    # def sent(self):
    # def confirm(self):

class Microphone():
    def __init__(self, pin = 32):
        self.microphone = ADC(Pin(pin))
        # adc1_config_width(ADC_WIDTH_BIT_12)
        # adc1_config_channel_atten(ADC1_CHANNEL_7, ADC_ATTEN_DB_11)
    
    #record one chunk of audio from the microphone
    #we can reliable send about 2000 samples per chunk and still have a reliable connection
    def readChunk(self, chunkSize = 1000):
        audioChunk = []
        for i in range(chunkSize):
            audioChunk.append(self.microphone.read_u16())
        return audioChunk

class Ldr():
    def __init__(self, pin = 21):
        self.pin = Pin(pin, Pin.IN)
        self.status = 0
    
    def checkStatus(self):
        #check if the jar has been lifted up
        if self.pin.value():
            return False
        return True

microphone = Microphone()
light = Light()
buzzer = Buzzer()
ldr = Ldr()


#The following line still has to be changed to assign handles automatically
oocsi = OOCSI('ThisVeryUniqueHandleAndSuch', 'oocsi.id.tue.nl')

def receiveEvent(sender, recipient, event):
    print('received ', event, ' from ', sender) #print the received message
    buzzer.play_received()
    light.applyColor(event['color'])

oocsi.subscribe('hearSayChannel', receiveEvent)

# keep the program running, can be quit with CTRL-C
counter = 0
muted = False
while True:
    sleep(1)
    # if ldr.checkStatus():
    #     if not muted:
    #         print("lifted")
    #         counter+=1
    #         if counter > 10:
                # counter = 0
    #             muted = True
    counter+=1
    if counter>10:
        counter = 0
        muted = True
    message = {}
    message['chunk'] = microphone.readChunk()
    message['flag'] = muted
    oocsi.send('hearSayServer', message)
    print('.')

    muted = False
    # else:
    #     print(".")
    #     muted = False
