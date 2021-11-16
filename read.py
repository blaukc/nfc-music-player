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
    while True:
        #sector = int(input("Enter sector number: "))
        id, text = reader.read(sector)
        #print(reader.read(sector))
        #print(text)

        try:
            while text[-1] == ' ':
                text = text[:-1]
            return text
        except:
            print('NFC tag read wrongly')


def playOnNFC(event, get_logger):
    logger = get_logger('NFC reader')
    logger.info('NFC tag listener process started')

    playlists = os.listdir(music_dir)
    now_playlist = ''

    while True:
        #reads playlist name sector on nfc tag
        nfc_playlist_name = read_sector(3)
        logger.info(nfc_playlist_name + ' tag read')

        #checks if tag read is in playlist list
        if nfc_playlist_name in playlists:
            #for first playlist or
            #if now playing nfc different from current nfc i.e. new playlist
            if now_playlist == '' or now_playlist != nfc_playlist_name:
                #now_playlist = nfc_playlist_name
                playlist_dir = os.path.join(music_dir, nfc_playlist_name)
                shuffle = (read_sector(4) == 'True')

                if now_playlist == '':
                    logger.info('Updating events to add and play first playlist: ' + nfc_playlist_name)
                    event['add_playlist'] = [True, playlist_dir, shuffle]

                elif now_playlist != nfc_playlist_name:
                    logger.info('Updating events to stop current playlist and play new playlist: ' + nfc_playlist_name)
                    event['new_playlist'] = [True, playlist_dir, shuffle]

                now_playlist = nfc_playlist_name

            else:
                time.sleep(1)

        else:
            logger.warning('tag playlist ' + nfc_playlist_name + ' is not in list of playlists')


def eventListener(event, get_logger):
    logger = get_logger('Event listener')
    logger.info('Event listener process started')
    #print('Event Listener process started')
    player = VLC()

    #checks if there is changes in the event manager, then executes changes to VLC player
    while True:
        try:
            if event['play']:
                event['play'] = False
                logger.info('Event heard: Playing')
                player.play()
                time.sleep(0.5)

            if event['add_playlist'][0]:
                event['add_playlist'] = [False, event['add_playlist'][1], event['add_playlist'][2]]
                logger.info('Event heard: Adding Playlist and Playing')
                player.addPlaylist(event['add_playlist'][1], event['add_playlist'][2])
                player.play()
                time.sleep(0.5)

            if event['new_playlist'][0]:
                event['new_playlist'] = [False, event['new_playlist'][1], event['new_playlist'][2]]
                logger.info('Event heard: Stopping')
                player.stop()
                logger.info('Event heard: Adding New Playlist and Playing')
                player.addPlaylist(event['new_playlist'][1], event['new_playlist'][2])
                player.play()
                time.sleep(0.5)

            if event['pause']:
                event['pause'] = False
                logger.info('Event heard: Pausing')
                player.pause()
                time.sleep(0.5)

            if event['next']:
                event['next'] = False
                logger.info('Event heard: Playing Next Song')
                player.next()
                time.sleep(0.5)

            if event['previous']:
                event['previous'] = False
                logger.info('Event heard: Playing Previous Song')
                player.previous()
                time.sleep(0.5)

        except Exception as e:
            print(e)
            logger.warning(e)
            logger.warning('Possible due to next/prev/pause pressed before music starts or error with vlc player')
        finally:
            time.sleep(0.5)



#GPIO buttons for next, previous, pause
# buttons = [13, 19, 26]
#
# #event manager
# event_dict = {
#     'play': False,
#     'add_playlist': [False, '', False],
#     'stop': False,
#     'pause': False,
#     'next': False,
#     'previous': False
# }
#
# def start():
#     try:
#         # multiprocessing manager used to keep shared variables
#         with multiprocessing.Manager() as manager:
#             event = manager.dict(event_dict)
#             pool = multiprocessing.Pool(processes=5)
#             # add NFC reader to process pool
#             pool.apply_async(playOnNFC, args=(event, ))
#
#             # add next, previous, pause button listeners to process pool
#             for button in buttons:
#                 pool.apply_async(GPIObutton.buttonLoop, args=(button, event))
#
#             # add event listener to process pool
#             pool.apply_async(eventListener, args=(event, ))
#
#             # while True:
#             #     pass
#     except KeyboardInterrupt:
#         print('KeyboardInterrupt')
#     finally:
#         pool.close()
#         pool.terminate()
#         pool.join()
#         print('Processes joined')
#         GPIO.cleanup()
#         print('GPIO cleanup')
