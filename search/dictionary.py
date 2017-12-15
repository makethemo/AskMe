#파이썬 json 파싱
#파이썬 html tag 제거 (정규표현식)

# 네이버 검색 Open API 예제 - 블로그 검색
import os, sys, urllib.request, json, re

client_id = "ABu4jsdB34K0KN1lSS_p"
client_secret = "6FJFuMHn0d"
input_text = "종이"
encText = urllib.parse.quote(input_text)
url = "https://openapi.naver.com/v1/search/encyc.json?display=1&query=" + encText # json 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()

if(rescode==200):
    response_body = response.read()
    dict = json.loads(response_body.decode('utf-8'))
    list = dict['items']
    description = list[0]
    result = description['description']
    result2 = re.sub('</*b>|[[]|[]]|[(]|[)]|[-]', '', result)
    result3 = re.findall('^.*?[.]', result2)
    print(result3[0])
else:
    print("Error Code:" + rescode)
