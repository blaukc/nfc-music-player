import RPi.GPIO as GPIO
import time

#initialises GPIO buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buttonLoop(gpio_num, event):
    print('GPIO button ' + str(gpio_num) + ' listener process started')
    paused = False

    #listens for button press, then changes the event manager
    #event manager changes detected by event listener
    while True:
        buttonState = GPIO.input(gpio_num)
        if not buttonState:
            if gpio_num == 13:
                event['next'] = True
                print('Next')

            if gpio_num == 19:
                event['previous'] = True
                print('Previous')

            if gpio_num == 26:
                if paused:
                    event['play'] = True
                    paused = True
                    print('Play')
                else:
                    event['pause'] = True
                    paused = False
                    print('Pause')

            time.sleep(1)
