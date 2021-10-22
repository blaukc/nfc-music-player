#!/usr/bin/env python

import RPi.GPIO as GPIO
from MFRC522 import SimpleMFRC522
import time
import os
from playmusic import VLC

reader = SimpleMFRC522()

music_dir = '/home/pi/Music'

def read(sector):
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
    playlists = os.listdir(music_dir)
    now_playing = False
    now_playlist = ''

    while True:
        nfc_playlist_name = read(3)
        if now_playlist == '':
            now_playlist = nfc_playlist_name

        if nfc_playlist_name in playlists and now_playlist == nfc_playlist_name:
            if not now_playing:
                playlist_dir = os.path.join(music_dir, nfc_playlist_name)
                shuffle = (read(4) == 'True')
                player = VLC(playlist_dir, shuffle)
                player.play()
                now_playing = True
            else:
                pass
        else:
            player.stop()
            now_playlist = nfc_playlist_name
            now_playing = False
        time.sleep(1)
        print(now_playing, now_playlist)

finally:
    GPIO.cleanup()
