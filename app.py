from time import sleep, perf_counter
import RPi.GPIO as GPIO

from dialog.detect_intent_stream import talk_to_dialogflow
from speech.recorder import get_recorder


def new_filename():
    import datetime
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.OUT)
    
    rec = get_recorder()
    rec.init()

    start_time = 0
    pushed = False

    try:
        while True:
            button_state = GPIO.input(18)
            if not button_state:
                GPIO.output(24, True)  # LED on
                # print('Button pressed...')

                if not pushed:
                    start_time = perf_counter()
                    pushed = True
                    rec.start_recording()

                sleep(0.2)
            else:
                GPIO.output(24, False)  # LED off
                rec.stop_recording()

                pushed = False
                if perf_counter() - start_time < 2:
                    rec.clear()
                    continue

                filename = new_filename()
                rec.save(filename)
                talk_to_dialogflow(filename)
    except:
        GPIO.cleanup()
