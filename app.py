from time import sleep
import RPi.GPIO as GPIO
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TTS_DIR = os.path.join(os.path.join(ROOT_DIR, 'speech'), '.tts')
PICTURES_DIR = os.path.join(ROOT_DIR, '.pictures')
KEY_PATH = os.path.join(ROOT_DIR, 'key.json')


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.OUT)
    
    try:
        while True:
            button_state = GPIO.input(18)
            if button_state == False:
                GPIO.output(24, True)  # LED on
                # print('Button pressed...')
                # TODO: implement record
                sleep(0.2)
            else:
                GPIO.output(24, False)  # LED off
    except:
        GPIO.cleanup()

