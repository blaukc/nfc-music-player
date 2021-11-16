import RPi.GPIO as GPIO
import time

#initialises GPIO buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buttonLoop(gpio_num, event, get_logger):
    logger = get_logger('GPIO'+ str(gpio_num))
    logger.info('GPIO button ' + str(gpio_num) + ' listener process started')
    #print('GPIO button ' + str(gpio_num) + ' listener process started')

    paused = False

    #listens for button press, then changes the event manager
    #event manager changes detected by event listener
    while True:
        buttonState = GPIO.input(gpio_num)
        if not buttonState:
            logger.info('Button ' + str(gpio_num) + ' pressed')

            if gpio_num == 13:
                event['next'] = True
                paused = False
                #print('Next')
                logger.info('Updating events to play next song')

            if gpio_num == 19:
                event['previous'] = True
                paused = False
                #print('Previous')
                logger.info('Updating events to play previous song')

            if gpio_num == 26:
                if paused:
                    event['play'] = True
                    paused = False
                    #print('Play')
                else:
                    event['pause'] = True
                    paused = True
                    #print('Pause')
                logger.info('Updating events to play/pause')

            time.sleep(1)
