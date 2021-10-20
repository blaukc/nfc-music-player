import threading
import time
import evdev
import vlc
# device /dev/input/event1, name "Swisscom RC", phys "AA:BB:CC:DD:EE:FF"




def readpause():
    device = evdev.InputDevice('/dev/input/event0')
    print(device)
    print('start readpause')
    while True:
        if 200 in device.active_keys():
            print('yeet')
            pause = True

def listen():
    device = evdev.InputDevice('/dev/input/event0')
    print(device)
    pause = False
    # device /dev/input/event1, name "Swisscom RC", phys "AA:BB:CC:DD:EE:FF"
    for event in device.read_loop():
        if event.code == 200 and event.value == 0:      #event.value == 0 (key up)
            if pause:
                pause = False
                print('unpaused')
                with open('pause.txt', 'w') as file:
                    file.write('unpause')
            else:
                pause = True
                print('paused')
                with open('pause.txt', 'w') as file:
                    file.write('pause')


def playsong():
    p = vlc.MediaPlayer("/home/pi/Music/212/Jeremy Zucker - i-70.mp3")
    p.play()
    # while True:
    #     time.sleep(1)
    #     print('1')
    #     if pause:
    #         p.pause()

# p = vlc.MediaPlayer("/home/pi/Music/212/Jeremy Zucker - i-70.mp3")
#
# p.play()
# x = threading.Thread(target=listen)
# x.start()
listen()

# y = threading.Thread(target=playsong)
# y.start()
