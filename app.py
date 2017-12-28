from time import sleep, perf_counter
import RPi.GPIO as GPIO

import pyaudio
import wave
import path
import os

from dialog.detect_intent_stream import talk_to_dialogflow
from speech.recorder import Recorder
from speech.clova import tts

import vlc


def new_filename():
    import datetime
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)  # Broadcom chip-specific 기준의 pin 번호
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 버튼 pin
    GPIO.setup(24, GPIO.OUT)  # LED pin

    # rec = Recorder()
    # rec.initialize()

    start_time = 0
    pushed = False
    is_recording = False

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 4

    p = pyaudio.PyAudio()

    try:
        """
        반복문 안에서 버튼이 눌렸을 때, 4초간 녹음 후 저장
        녹음된 파일을 dialog 패키지에서 처리
        결과값을 Text-to-speech 로 저장 후 재생 
        """
        while True:
            button_state = GPIO.input(18)
            if not button_state:
                GPIO.output(24, True)  # LED on
                print('Button pressed...')

                if not is_recording:
                    stream = p.open(format=FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True,
                                    frames_per_buffer=CHUNK)

                    print("* recording")

                    frames = []

                    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                            data = stream.read(CHUNK)
                            frames.append(data)

                    print("* done recording")

                    stream.stop_stream()
                    stream.close()
                    # p.terminate()

                    filename = os.path.join(path.MIC_DIR, new_filename())

                    with wave.open(filename, 'wb') as wf:
                        wf.setnchannels(CHANNELS)
                        wf.setsampwidth(p.get_sample_size(FORMAT))
                        wf.setframerate(RATE)
                        wf.writeframes(b''.join(frames))
                        wf.close()

                    player = vlc.MediaPlayer(tts(talk_to_dialogflow(filename)))
                    player.play()

                    is_recording = False

                sleep(0.2)
            else:
                GPIO.output(24, False)  # LED off
                pushed = False

    except Exception as e:
        p.terminate()
        GPIO.cleanup()
        print(e)

    p.terminate()
    GPIO.cleanup()
