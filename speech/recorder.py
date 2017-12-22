#!/usr/bin/env python3
from time import sleep
import pyaudio
import wave

CHUNK = 512
FORMAT = pyaudio.paInt16  # paInt8
CHANNELS = 1
RATE = 16000  # sample rate


class Recorder:

    def __init__(self):
        self.p = None
        self.stream = None
        self.frames = []
        self.pause = False

    def initialize(self):
        self.p = pyaudio.PyAudio()

    def start_recording(self):
        self.pause = False
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)  # buffer

        print("* recording")
        
        try:
            while not self.pause:
                data = self.stream.read(CHUNK)
                self.frames.append(data) # 2 bytes(16 bits) per channel
                sleep(0.1)
        except Exception as e:
            print(e)


    def stop_recording(self):
        self.pause = True
        print("* done recording")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def clear(self):
        del self.frames[:]

    def save(self, filepath):
        if len(self.frames):
            print('Fail to save: frames is empty.')
            return

        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))
            del self.frames[:]
            wf.close()
