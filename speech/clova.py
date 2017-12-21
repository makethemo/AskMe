import datetime
import httplib2
import urllib
import json
import os

import app

http = httplib2.Http()
req_url = "https://openapi.naver.com/v1/voice/tts.bin"
error_file = os.path.join(app.TTS_DIR, 'error.mp3')

with open(app.KEY_PATH, 'r') as jsonFile:  # local API key store
    key = json.load(jsonFile)
    req_headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Naver-Client-Id": key['speech_client_id'],
        "X-Naver-Client-Secret": key['speech_client_secret']
    }


def get_time_for_filename():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


def new_filename():
    return os.path.join(app.TTS_DIR, get_time_for_filename() + '.mp3')


def tts(text):
    encText = urllib.parse.quote(text)
    req_body = "speaker=mijin&speed=0&text=" + encText
    (headers, body) = http.request(req_url, 'POST', body=req_body.encode('utf-8'), headers=req_headers)

    if headers['status'] == '200':
        filename = new_filename()
        with open(filename, 'wb') as f:
            f.write(body)
        return filename
    else:
        return error_file


if __name__ == '__main__':
    pass
    # tts("안녕하세요?")
