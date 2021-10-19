#!/usr/bin/env python

import RPi.GPIO as GPIO
from MFRC522 import SimpleMFRC522

reader = SimpleMFRC522([16, 17, 18])

try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
finally:
        GPIO.cleanup()
