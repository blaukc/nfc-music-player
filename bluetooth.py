import RPi.GPIO as GPIO
import time
import pexpect
import multiprocessing
import read
import GPIObutton
from VLCplayer import VLC

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#MAC address of bluetooth speaker
mac = 'B8:F6:53:9B:97:B4'

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

if __name__ == '__main__':
    try:
        while True:
            with multiprocessing.Manager() as manager:
                event = manager.dict(event_dict)
                pool = multiprocessing.Pool(processes=5)
                while True:
                    buttonState = GPIO.input(6)
                    if not buttonState:
                        print(6)
                        child = pexpect.spawn('bluetoothctl')
                        child.expect('Agent registered')
                        child.sendline('connect ' + mac)
                        # if 'Connected: yes' comes first, speaker is not yet connected
                        # if 'Connection successful' comes first, speaker is already connected
                        connected = child.expect(['Connected: yes', 'Connection successful'])
                        if connected == 0:
                            print('Connected')
                            # time.sleep(3)
                            # player = VLC()
                            # player.addPlaylist("/home/pi/Music/211/", True)
                            # player.play()
                            # print('playing')
                            # time.sleep(15)
                            # add NFC reader to process pool
                            pool.apply_async(read.playOnNFC, args=(event, ))

                            # add next, previous, pause button listeners to process pool
                            for button in buttons:
                                pool.apply_async(GPIObutton.buttonLoop, args=(button, event))

                            # add event listener to process pool
                            pool.apply_async(read.eventListener, args=(event, ))
                            print('pools!')
                            # while True:
                            #     pass
                        else:
                            child.sendline('disconnect ' + mac)
                            child.expect('Connected: no')
                            print('Disconnected')
                            pool.close()
                            pool.terminate()
                            pool.join()
                            print('Processes joined')
                            break
                        time.sleep(1)
            time.sleep(0.1)
    finally:
        GPIO.cleanup()
