#!/usr/bin/env python

import RPi.GPIO as GPIO
from MFRC522 import SimpleMFRC522

reader = SimpleMFRC522([16, 17, 18])

try:
        id, text = reader.read()
        print(id)
        print(text)
        print(reader.read())
finally:
        GPIO.cleanup()
