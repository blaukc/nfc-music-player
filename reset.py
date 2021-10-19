#!/usr/bin/env python

import RPi.GPIO as GPIO
from MFRC522 import SimpleMFRC522

reader = SimpleMFRC522([8, 9, 10])

try:
        print("Now place your tag to write")
        reader.reset()
        print("Reset")
finally:
        GPIO.cleanup()
