#!/usr/bin/env python

import RPi.GPIO as GPIO
from MFRC522 import SimpleMFRC522

reader = SimpleMFRC522([11, 12, 13])

try:
        id, text = reader.read()
        print(id)
        print(text)
        print(reader.read())
finally:
        GPIO.cleanup()
