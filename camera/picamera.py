import picamera
import datetime # 시스템 시간 가져오기 위한
from time import sleep


def picture():

    camera = picamera.PiCamera()
    camera.vflip = True
    camera.exposure_mode = 'auto'  # 노출
    t = datetime.datetime.now().strftime('%Y%m%d_%H%M_%S')  # 현재 시간
    camera.resolution = (1920, 1080) # 해상도
    camera.start_preview()
    sleep(1)
    file_name = t + '.jpg'
    camera.capture('../.pictures/' + file_name) #시스템 시간
    return file_name


def video():

    camera = picamera.PiCamera()
    camera.vflip = True
    camera.exposure_mode = 'auto'  # 노출
    t = datetime.datetime.now().strftime('%Y%m%d_%H%M_%S')  # 현재 시간
    camera.resolution = (1920, 1080)
    file_name = t + '.h264'
    camera.start_recording('../.pictures/' + file_name)
    sleep(10)
    camera.stop_recording()
    return file_name