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
ÀÌ¹ÌÁö¸¦ À¥À¸·Î Àü¼ÛÇÏ±â À§ÇØ ¹ÙÀÌÆ® ÄÚµå·Î º¯È¯
""" 
def encode_image(image_path, charset):
    with open(image_path, 'rb') as image:
        b64_img = b64encode(image.read())

    return b64_img.decode(charset)


"""
ÀÀ´ä¹ÞÀ» json¿ä¼ÒÀÇ typeÀ» ÁöÁ¤
À¥À¸·ÎºÎÅÍ Àü¼Û¹ÞÀº ÄÚµå(req_body)¸¦ json ¹®ÀÚ¿­·Î ÀÎÄÚµù
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
ÀÌ¹ÌÁö¿¡¼­ ´ë»óÀ» ÀÎ½ÄÇÏ°íÀÚ ÇÏ´Â °æ¿ì
¾Æ·¡ Á¶°ÇÀ» ÃæÁ·ÇÏ´Â label¿ä¼Ò¸¸ ÀúÀå

È®·üÀÌ 60% ÀÌ»óÀÎ ¿ä¼Ò¸¸ ¸ð¾Æ Æò±Õ È®·üÀ» ±¸ÇÔ
Æò±Õ È®·üÀÌ 75% ÀÌ»óÀÏ¶§ °³º° È®·üÀÌ 80% ÀÌ»óÀÎ ¿ä¼Ò¸¸ ÀúÀå
Æò±Õ È®·üÀÌ 75% ¹Ì¸¸ÀÏ¶§ °³º° È®·üÀÌ 70% ÀÌ»óÀÎ ¿ä¼Ò¸¸ ÀúÀå
""" 
def image_label_detection(data):
    label = []
    score = []
    length = len(data["responses"][0]["labelAnnotations"])

    for i in range(length):  # labelê³¼ ê·¸ì— ëŒ€ì‘í•˜ëŠ” score ì €ìž¥
        if data["responses"][0]["labelAnnotations"][i]["score"] > 0.6:
            label.append(data["responses"][0]["labelAnnotations"][i]["description"])
            score.append(data["responses"][0]["labelAnnotations"][i]["score"])
            if label[len(label)-1] == "product" or label[len(label)-1] == "produce":
                label.pop()
                label.append(data["responses"][0]["webDetection"]["webEntities"][0]["description"])

    length = len(label)

    # ì¡°ê±´ì— ë§žê²Œ label ìž˜ë¼ë‚´ê¸°
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
ÀÌ¹ÌÁö¿¡¼­ ±ÛÀÚ¸¦ ÀÎ½ÄÇÏ°íÀÚ ÇÏ´Â °æ¿ì
textAnnotationÀÇ Ã¹¹øÂ° descriptionÀ» ±×´ë·Î ¹ÝÈ¯
""" 
def image_text_detection(data):
    return data["responses"][0]["textAnnotations"][0]["description"]


"""
¿ÜºÎ¿¡¼­ ¿Â ¹ÙÀÌÆ® ÄÚµå¸¦ json ¹®ÀÚ¿­·Î º¯È¯ÇÏ°í - json.dumps
ÀÌ¸¦ ÆÄÀÌ½ã ³»¿¡¼­ »ç¿ëÇÒ ¶§ json °´Ã¼·Î º¯È¯ÇÏ´Â °úÁ¤ - json.loads

get_label - label ¿ä¼Ò¸¦ ¹ÝÈ¯ÇÒ ¶§ »ç¿ë
get_text - ±ÛÀ» ÀÐÀ»¶§ ÅØ½ºÆ® ¹ÝÈ¯¿¡ »ç¿ë 
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
