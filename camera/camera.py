from time import sleep
import picamera
import datetime  # 시스템 시간 가져오기 위한
import os

import path

camera = picamera.PiCamera()
camera.vflip = True  # 카메라 상하 반전
camera.exposure_mode = 'auto'  # 노출
camera.resolution = (1920, 1080)  # 해상도


def get_time_for_filename():  # 현재시간을 파일 이름으로
    return datetime.datetime.now().strftime('%Y%m%d_%H%M_%S')  # 현재 시간


def start_preview():  # 미리보기 시작
    camera.start_preview()


def stop_preview():  # 미리보기 중지
    camera.stop_preview()


def take_a_picture():  # 사진찍기
    file_name = get_time_for_filename() + '.jpg'
    file_path = os.path.join(path.PICTURES_DIR, file_name)
    camera.capture(file_path)  # 시스템 시간
    return file_path


def take_a_video(seconds):  # 비디오 찍기
    file_name = get_time_for_filename() + '.h264'
    file_path = os.path.join(path.PICTURES_DIR, file_name)
    camera.start_recording(file_path)
    sleep(seconds)
    camera.stop_recording()
    return file_path
