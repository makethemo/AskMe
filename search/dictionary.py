import urllib.request, json, re

import path

with open(path.KEY_PATH, 'r') as data_file:
    data = json.load(data_file)


def search_keyword_by_naver_dic(input_text):
    client_id = data['search_api-id']
    client_secret = data['search_api-secret']
    encText = urllib.parse.quote(input_text)
    url = "https://openapi.naver.com/v1/search/encyc.json?display=1&query=" + encText  # json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if rescode == 200:
        response_body = response.read()
        dict = json.loads(response_body.decode('utf-8'))
        list = dict['items']
        result = list[0]
        result2 = result['description']
        result3 = re.sub('</*b>|[[]|[]]|[(]|[)]|[-]', '', result2)
        result4 = re.findall('^.*?[.]', result3)
        description = result4[0]
        return description
    else:
        # print("Error Code:" + rescode)
        return '해당 내용을 찾을 수 없습니다.'


if __name__ == '__main__':
    """
    테스트 코드
    """
    search_keyword_by_naver_dic('백과사전')
