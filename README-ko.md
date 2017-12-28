# AskMe
[\[ English \]](https://github.com/makethemo/AskMe/blob/develop/README.md)

라즈베리파이3를 활용한 음성 및 영상 인식

## Introduction

마이크로 녹음한 음성을 Dialogflow를 통해 아래 기능으로 분기합니다.

현재 한국어 음성만 지원합니다.

- "앞에 뭐 있어?"
  - `camera/camera.py` 에서 사진을 찍고, 파일경로를 반환
  - `vision/vision_api_request.py` 에서 Google Cloud Vision API 요청
  - 응답한 결과를 `translate/papago.py` 에서 한국어로 변역
  - `dialog/detect_intent_stream.py` 에서 문장화
  - `speech/clova.py` 에서 음성 합성
- "xx 검색해줘."
  - Dialogflow에서 얻은 키워드로 `search/dictionary.py` 에서 백과사전 검색
  - 검색 결과를 `speech/clova.py` 에서 읽어줌
- "xx 날씨 어때?"
  - Dialogflow에서 키워드를 얻음
  - `weather/request_weather.py` 에서 날씨 정보 요청
  - 응답 결과를 `speech/clova.py` 에서 읽어줌


## License
```
Copyright 2017 Jinseop Mo, Hyeonwoo Kim, Hyeonjun Kim, Haneul Lee, Gyeongyun Jeong

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
