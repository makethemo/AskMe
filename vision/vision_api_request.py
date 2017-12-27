from base64 import b64encode
import httplib2
import json

import path

http = httplib2.Http()

base_url = 'https://vision.googleapis.com/v1/images:annotate?key='

with open(path.KEY_PATH, 'r') as jsonFile:  # local API key store
    key = json.load(jsonFile)
    req_url = base_url + key['vision_api-key']


"""
�̹����� ������ �����ϱ� ���� ����Ʈ �ڵ�� ��ȯ
""" 
def encode_image(image_path, charset):
    with open(image_path, 'rb') as image:
        b64_img = b64encode(image.read())

    return b64_img.decode(charset)


"""
������� json����� type�� ����
�����κ��� ���۹��� �ڵ�(req_body)�� json ���ڿ��� ���ڵ�
""" 
def get_response(b64encoded_image):
    req_body = {
      "requests": [
        {
          "image": {
            "content": b64encoded_image
          },
          "features": [
            {
                "type": "LABEL_DETECTION",
                "maxResults": 15
            },
            {
                "type" : "TEXT_DETECTION",
                "maxResults": 1
            },
            {
                "type" : "WEB_DETECTION",
                "maxResults": 1
            }
          ]
        }
      ]
    }

    req_headers = {"Content-Type": "application/json; charset=utf-8"}

    (headers, body) = http.request(req_url, 'POST', body=json.dumps(req_body), headers=req_headers)
    return headers, body


"""
�̹������� ����� �ν��ϰ��� �ϴ� ���
�Ʒ� ������ �����ϴ� label��Ҹ� ����

Ȯ���� 60% �̻��� ��Ҹ� ��� ��� Ȯ���� ����
��� Ȯ���� 75% �̻��϶� ���� Ȯ���� 80% �̻��� ��Ҹ� ����
��� Ȯ���� 75% �̸��϶� ���� Ȯ���� 70% �̻��� ��Ҹ� ����
""" 
def image_label_detection(data):
    label = []
    score = []
    length = len(data["responses"][0]["labelAnnotations"])

    for i in range(length):  # label과 그에 대응하는 score 저장
        if data["responses"][0]["labelAnnotations"][i]["score"] > 0.6:
            label.append(data["responses"][0]["labelAnnotations"][i]["description"])
            score.append(data["responses"][0]["labelAnnotations"][i]["score"])
            if label[len(label)-1] == "product" or label[len(label)-1] == "produce":
                label.pop()
                label.append(data["responses"][0]["webDetection"]["webEntities"][0]["description"])

    length = len(label)

    # 조건에 맞게 label 잘라내기
    if score[0] > 0.95:
        while score[length-1] < 0.95:
            label.pop()
            length = len(label)
    elif sum(score)/length > 0.75:
        while score[length-1] < 80:
            label.pop()
            length = len(label)
    else:
        while score[length-1] < 70:
            label.pop()
            length = len(label)

    return label


"""
�̹������� ���ڸ� �ν��ϰ��� �ϴ� ���
textAnnotation�� ù��° description�� �״�� ��ȯ
""" 
def image_text_detection(data):
    return data["responses"][0]["textAnnotations"][0]["description"]


"""
�ܺο��� �� ����Ʈ �ڵ带 json ���ڿ��� ��ȯ�ϰ� - json.dumps
�̸� ���̽� ������ ����� �� json ��ü�� ��ȯ�ϴ� ���� - json.loads

get_label - label ��Ҹ� ��ȯ�� �� ���
get_text - ���� ������ �ؽ�Ʈ ��ȯ�� ��� 
"""
def get_label(local_image_path):
    (headers, body) = get_response(encode_image(local_image_path, 'ascii'))
    data = json.loads(body.decode('utf-8'))
    return image_label_detection(data)


def get_text(local_image_path):
    (headers, body) = get_response(encode_image(local_image_path, 'ascii'))
    data = json.loads(body.decode('utf-8'))
    return image_text_detection(data)


if __name__ == '__main__':
    local_image_path = "./orange.jpg"    # You have to fix the image path here.
    (headers, body) = get_response(encode_image(local_image_path, 'ascii'))

    data = json.loads(body.decode('utf-8'))
    image_label_detection(data)

    image_text_detection(data)

    print(data["responses"][0]["labelAnnotations"][0]["description"])
