# AskMe
[\[ 한국어 \]](https://github.com/makethemo/AskMe/blob/develop/README-ko.md)

Image and speech recognition on Raspberry Pi 3

## Introduction

The voice recorded by microphones is diverted to the following function through Dialogflow.

Currently, only Korean audio is supported.

- "What's in front of you?"
  - It takes a picture in `camera/camera.py` and returns the path.
  - Google Cloud Vision API is requested in `vision/vision_api_request.py`.
  - `translate/papago.py` translates the response result into Korean.
  - `dialog/detect_intent_stream.py` makes it a sentence.
  - Speech synthesis in `speech/clova.py`.
- "Search xx."
  - It searches encyclopedia through `search/dictionary.py` with keywords from Dialogflow.
  - It reads results from `speech/clova.py`.
- "How about the weather in xx?"
  - It gets keywords from Dialogflow.
  - It requests weather information through `weather/request_weather.py`.
  - It reads the response from `speech/clova.py`.

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
