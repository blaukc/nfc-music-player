import RPi.GPIO as GPIO
import time
import multiprocessing

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# while True:
#     buttonState1 = GPIO.input(6)
#     buttonState2 = GPIO.input(13)
#     buttonState3 = GPIO.input(19)
#     buttonState4 = GPIO.input(26)
#     if not buttonState1:
#         print('6')
#         time.sleep(1)
#     if not buttonState2:
#         print('13')
#         time.sleep(1)
#     if not buttonState3:
#         print('19')
#         time.sleep(1)
#     if not buttonState4:
#         print('26')
#         time.sleep(1)

def buttonLoop(gpio_num):
    print('button on')
    while True:
        buttonState = GPIO.input(gpio_num[0])
        if not buttonState:
            print(gpio_num[1])
            time.sleep(1)

# buttons = [[6, 'Bluetooth'], [13, 'Next'], [19, 'Previous'], [26, 'Play/Pause']]
#
# try:
#     pool = multiprocessing.Pool()
#     processes = pool.map(buttonLoop, buttons)
# finally:
#     pool.close()
#     pool.join()
