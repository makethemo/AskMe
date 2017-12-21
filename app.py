from time import sleep
import RPi.GPIO as GPIO
import os

from speech.recorder import get_recorder

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TTS_DIR = os.path.join(os.path.join(ROOT_DIR, 'speech'), '.tts')
MIC_DIR = os.path.join(ROOT_DIR, '.mic')
PICTURES_DIR = os.path.join(ROOT_DIR, '.pictures')
KEY_PATH = os.path.join(ROOT_DIR, 'key.json')


def new_filename():
    import datetime
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.OUT)
    
    rec = get_recorder()
    rec.init()
    
    # TODO: time count

    try:
        while True:
            button_state = GPIO.input(18)
            if button_state == False:
                GPIO.output(24, True)  # LED on
                # print('Button pressed...')
                rec.start_recording()
                sleep(0.2)
            else:
                GPIO.output(24, False)  # LED off
                rec.stop_recording()
                filename = new_filename()
                rec.save(filename)
                # TODO call dialogflow
    except:
        GPIO.cleanup()

