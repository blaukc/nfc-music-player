#!/usr/bin/env python

import RPi.GPIO as GPIO
from MFRC522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    sector = int(input("Enter sector number: "))
    id, text = reader.read(sector)
    print(id)
    print(text)
finally:
    GPIO.cleanup()
