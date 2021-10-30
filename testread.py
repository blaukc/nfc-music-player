import RPi.GPIO as GPIO
from MFRC522 import SimpleMFRC522

reader = SimpleMFRC522()

def read_sector(sector):
    #sector = int(input("Enter sector number: "))
    id, text = reader.read(sector)
    #print(reader.read(sector))
    #print(text)

    try:
        while text[-1] == ' ':
            text = text[:-1]
    except:
        print('NFC tag read wrongly')

    return text

try:
        print(read_sector(3))
finally:
        GPIO.cleanup()
