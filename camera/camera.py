from time import sleep
import picamera
import datetime  # 시스템 시간 가져오기 위한
import os

import app

camera = picamera.PiCamera()
camera.vflip = True
camera.exposure_mode = 'auto'  # 노출
camera.resolution = (1920, 1080)  # 해상도


def get_time_for_filename():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M_%S')  # 현재 시간


def start_preview():
    camera.start_preview()


def stop_preview():
    camera.stop_preview()


def take_a_picture():
    file_name = get_time_for_filename() + '.jpg'
    camera.capture(os.path.join(app.PICTURES_DIR, file_name))  # 시스템 시간
    return file_name


def take_a_video(seconds):
    file_name = get_time_for_filename() + '.h264'
    camera.start_recording(os.path.join(app.PICTURES_DIR, file_name))
    sleep(seconds)
    camera.stop_recording()
    return file_name
