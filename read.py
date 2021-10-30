#!/usr/bin/env python

import RPi.GPIO as GPIO
from MFRC522 import SimpleMFRC522
import time
import os
import multiprocessing
from VLCplayer import VLC
import GPIObutton

reader = SimpleMFRC522()

music_dir = '/home/pi/Music'


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


def playOnNFC(event):
    try:
        playlists = os.listdir(music_dir)
        now_playing = False
        now_playlist = ''

        while True:
            #reads playlist name sector on nfc tag
            nfc_playlist_name = read_sector(3)
            if now_playlist == '':
                now_playlist = nfc_playlist_name

            if nfc_playlist_name in playlists and now_playlist == nfc_playlist_name:
                #if no track playing currently
                if not now_playing:
                    playlist_dir = os.path.join(music_dir, nfc_playlist_name)
                    shuffle = (read_sector(4) == 'True')

                    #triggers event manager to add playlist to VLC player
                    event['add_playlist'] = [True, playlist_dir, shuffle]

                    now_playing = True
                    time.sleep(1)

                #if playlist playing now is the same
                else:
                    time.sleep(1)

            #if change in playlist, stop the current playlist
            else:
                event['stop'] = True
                now_playlist = nfc_playlist_name
                now_playing = False

            print(now_playing, now_playlist)
    finally:
        GPIO.cleanup()
        print('cleanup')


def eventListener(event):
    print('Event Listener process started')
    player = VLC()

    #checks if there is changes in the event manager, then executes changes to VLC player
    while True:
        try:
            if event['play']:
                event['play'] = False
                player.play()
                time.sleep(0.5)

            if event['add_playlist'][0]:
                event['add_playlist'] = [False, event['add_playlist'][1], event['add_playlist'][2]]
                print('yes')
                print(event)
                player.addPlaylist(event['add_playlist'][1], event['add_playlist'][2])
                player.play()
                time.sleep(0.5)

            if event['stop']:
                event['stop'] = False
                player.stop()
                time.sleep(0.5)

            if event['pause']:
                event['pause'] = False
                player.pause()
                time.sleep(0.5)

            if event['next']:
                event['next'] = False
                player.next()
                time.sleep(0.5)

            if event['previous']:
                event['previous'] = False
                player.previous()
                time.sleep(0.5)
        except Exception as e:
            print(e)



#GPIO buttons for next, previous, pause
buttons = [13, 19, 26]

#event manager
event_dict = {
    'play': False,
    'add_playlist': [False, '', False],
    'stop': False,
    'pause': False,
    'next': False,
    'previous': False
}

try:
    # multiprocessing manager used to keep shared variables
    with multiprocessing.Manager() as manager:
        event = manager.dict(event_dict)
        pool = multiprocessing.Pool(processes=5)
        # add NFC reader to process pool
        pool.apply_async(playOnNFC, args=(event, ))

        # add next, previous, pause button listeners to process pool
        for button in buttons:
            pool.apply_async(GPIObutton.buttonLoop, args=(button, event))

        # add event listener to process pool
        pool.apply_async(eventListener, args=(event, ))

        while True:
            pass
except KeyboardInterrupt:
    print('KeyboardInterrupt')
finally:
    pool.close()
    pool.join()
    print('Processes joined')
    GPIO.cleanup()
    print('GPIO cleanup')
