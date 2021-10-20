#!/usr/bin/env python

import RPi.GPIO as GPIO
from MFRC522 import SimpleMFRC522
import time
from pygame import mixer

reader = SimpleMFRC522()

try:
    sector = int(input("Enter sector number: "))
    id, text = reader.read(sector)
    print(reader.read(sector))
    print(text)
finally:
    GPIO.cleanup()

while text[-1] == ' ':
    text = text[:-1]

if text == 'i-70':
    print('playing music')
    mixer.init()
    mixer.music.load("/home/pi/Music/212/Jeremy Zucker - i-70.mp3")
    mixer.music.play()
    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)
    print('song end')
