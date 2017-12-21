#!/usr/bin/env python3
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16 #paInt8
CHANNELS = 1
RATE = 16000 #sample rate


def get_recorder():
    p = None
    frames = []
    pause = False


    def init():
        p = pyaudio.PyAudio()


    def start_recording():
        pause = False
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK) #buffer

        print("* recording")

        while not pause:
            data = stream.read(CHUNK)
            frames.append(data) # 2 bytes(16 bits) per channel


    def stop_recording():
        pause = True
        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()


    def clear():
        del frames[:]


    def save(filepath):
        if len(frames):
            print('Fail to save: frames is empty.')
            return

        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            del frames[:]
            wf.close()

