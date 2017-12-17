from base64 import b64encode
import httplib2
import json

http = httplib2.Http()

base_url = 'https://vision.googleapis.com/v1/images:annotate?key='


def encode_image(image_path, charset):
    with open(image_path, 'rb') as image:
        b64_img = b64encode(image.read())

    return b64_img.decode(charset)


def get_response(b64encoded_image):
    with open('key.json', 'r') as jsonFile:    # local API key store
        key = json.load(jsonFile)
        req_url = base_url + key['api-key']

    req_body = {
      "requests": [
        {
          "image": {
            "content": b64encoded_image
          },
          "features": [
            {
              "type": "LABEL_DETECTION",
              "maxResults": 1
            }
          ]
        }
      ]
    }

    req_headers = {"Content-Type": "application/json; charset=utf-8"}

    (headers, body) = http.request(req_url, 'POST', body=json.dumps(req_body), headers=req_headers)
    return headers, body


if __name__ == '__main__':
    local_image_path = 'local_image.jpg'    # You have to fix the image path here.

    (headers, body) = get_response(encode_image(local_image_path, 'ascii'))

    print(body.decode('utf-8'))
