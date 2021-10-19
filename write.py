#!/usr/bin/env python

import RPi.GPIO as GPIO
from MFRC522 import SimpleMFRC522

reader = SimpleMFRC522([12, 13, 14])

try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
finally:
        GPIO.cleanup()
