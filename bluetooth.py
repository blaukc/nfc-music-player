import RPi.GPIO as GPIO
import time
import pexpect
import multiprocessing
import read
import GPIObutton
from VLCplayer import VLC
import logging

def get_logger(name):
    log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        filename='dev.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)

logger = get_logger('main')

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
    'new_playlist': [False, '', False],
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
                        logging.info('Button 6 Pressed')
                        print('Connect/Disconnect')
                        child = pexpect.spawn('bluetoothctl')
                        child.expect('Agent registered')
                        child.sendline('connect ' + mac)
                        # if 'Connected: yes' comes first, speaker is not yet connected
                        # if 'Connection successful' comes first, speaker is already connected
                        connected = child.expect(['Connected: yes', 'Connection successful'])
                        if connected == 0:
                            logging.info('Bluetooth connected')
                            print('Connected')
                            # time.sleep(3)
                            # player = VLC()
                            # player.addPlaylist("/home/pi/Music/211/", True)
                            # player.play()
                            # print('playing')
                            # time.sleep(15)
                            # add NFC reader to process pool
                            pool.apply_async(read.playOnNFC, args=(event, get_logger, ))

                            # add next, previous, pause button listeners to process pool
                            for button in buttons:
                                pool.apply_async(GPIObutton.buttonLoop, args=(button, event, get_logger, ))

                            # add event listener to process pool
                            pool.apply_async(read.eventListener, args=(event, get_logger, ))
                            print('pools!')
                            logging.info('All processes started')
                            # while True:
                            #     pass
                        else:
                            child.sendline('disconnect ' + mac)
                            child.expect('Connected: no')
                            print('Disconnected')
                            logging.info('Bluetooth disconnected')
                            pool.close()
                            pool.terminate()
                            pool.join()
                            print('Processes joined')
                            logging.info('Processes joinedpy')
                            break
                        time.sleep(1)
            time.sleep(0.1)
    finally:
        GPIO.cleanup()
