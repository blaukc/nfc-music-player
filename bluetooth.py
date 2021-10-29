import RPi.GPIO as GPIO
import time
import pexpect

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
mac = 'B8:F6:53:9B:97:B4'

while True:
    buttonState = GPIO.input(6)
    if not buttonState:
        print(6)
        child = pexpect.spawn('bluetoothctl')
        child.expect('Agent registered')
        child.sendline('connect ' + mac)
        # if 'Connected: yes' comes first, speaker is not yet connected
        # if 'Connection successful' comes first, speaker is already connected
        connected = child.expect(['Connected: yes', 'Connection successful'])
        if connected == 0:
            print('Connected')
        else:
            child.sendline('disconnect ' + mac)
            child.expect('Connected: no')
            print('Disconnected')
        time.sleep(1)
