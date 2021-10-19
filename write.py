#!/usr/bin/env python

import RPi.GPIO as GPIO
from MFRC522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    sector = input("Enter sector number: ")
    text = input('New data:')
    print("Now place your tag to write")
    reader.write(sector, text)
    print("Written")
finally:
        GPIO.cleanup()
