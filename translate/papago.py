import urllib.request

import path
import json

with open(path.KEY_PATH, 'r') as json_file:
    key = json.load(json_file)
    client_id = key['papago_client_id']
    client_secret = key['papago_client_secret']


def english_to_korean(text):
    encText = urllib.parse.quote(text)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/language/translate"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        return response_body.decode('utf-8')
    else:
        return '다시 한번 말씀해주세요.'
