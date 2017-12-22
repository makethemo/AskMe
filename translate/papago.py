import urllib.request

import path

with open(path.KEY_PATH, 'r') as key:
    client_id = key['papago_client_id']
    client_secret = key['papago_client_secret']

encText = urllib.parse.quote("Tree")
data = "source=en&target=ko&text=" + encText
url = "https://openapi.naver.com/v1/language/translate"

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
response = urllib.request.urlopen(request, data=data.encode("utf-8"))
rescode = response.getcode()


def english_to_korean(encText):
    print("번역된 한글입니다 : %s" %encText)
    if encText:
        print ("나무")

    else:
        print("Error Code:" + rescode)

    return
