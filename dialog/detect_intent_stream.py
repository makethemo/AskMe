from camera import camera
from vision import vision_api_request
from search import dictionary
from weather import request_weather
import dialogflow
import json
import httplib2

from translate.papago import english_to_korean
import path

http = httplib2.Http()

with open(path.KEY_PATH, 'r') as key_file:
    key = json.load(key_file)
    dialog_project_id = key['dialog_project_ID']
    dialog_session_id = key['dialog_session_ID']

def detect_intent_stream(project_id, session_id, audio_file_path, language_code):  # dialogflow intent에 접근

    session_client = dialogflow.SessionsClient()
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    def request_generator(audio_config, audio_file_path):  # 지정된경로의 음성파일에서 질문 의도 추출
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session, query_input=query_input)

        with open(audio_file_path, 'rb') as audio_file:  # 작은 덩어리단위로 쪼개어 인식 후 문장완성
            while True:
                chunk = audio_file.read(4096)
                if not chunk:
                    break
                yield dialogflow.types.StreamingDetectIntentRequest(
                    input_audio=chunk)

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)

    requests = request_generator(audio_config, audio_file_path)
    responses = session_client.streaming_detect_intent(requests)

    print('=' * 20)
    for response in responses:
        print('Intermediate transcript: "{}".'.format(response.recognition_result.transcript))

    query_result = response.query_result

    intent_name = format(query_result.intent.display_name)

    print('=' * 20)
    print('Query text: {}'.format(query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(query_result.intent.display_name, query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(query_result.fulfillment_text))
    # print('d:{}\n'.format(query_result))


    if intent_name == "picture":  # 사진찍기
        camera.take_a_picture()

    if intent_name == "video":  # 비디오찍기
        camera.take_a_video(10)

    if intent_name == "sight":  # "앞에 뭐가있어"에 대한 응답을 리턴
        picture = camera.take_a_picture()  # 사진 찍기
        labels = vision_api_request.get_label(picture)  # vision에 사진 전송
        print('labels: ', labels)
        # TODO labels list를 문장화 시켜서 리턴.
        """
        for i in range(len(labels)):  # vision에서 추출된 n개의 lables
            if i != len(labels) -1:
                label_str = label_str + labels[i] + ", "
            else:
                label_str = label_str + labels[i]
                label_str = label_str + "있습니다."
        """
        
        for i in range(len(labels)):  # vision에서 넘어온 단어의 개수만큼 출력
            labels[i] = json.loads(english_to_korean(labels[i]))['message']['result']['translatedText']

        print('translated labels:', labels)
        result = ' '.join(labels) +  "있습니다."
        print(result)
        return result

    if intent_name == "search":  # "검색해봐" 에 대한 응답을 인터넷에서 찾아 리턴
        key_word = query_result.fulfillment_text
        return dictionary.search_keyword_by_naver_dic(key_word)
    
    if intent_name == "c-weather":  # 날씨를 weather api를 통해 얻어서 리턴
        return request_weather.requestCurrentWeather('대전','대덕구', '중리동')
    
    """
    req_headers = {"Content-Type": "application/json; charset=utf-8"}

    (headers, body) = http.request(req_url, 'POST', body=json.dumps(req_body), headers=req_headers)
    return body.decode('utf-8')
    """

def talk_to_dialogflow(local_voice_path):  # dialogflow
    return detect_intent_stream(dialog_project_id, dialog_session_id, local_voice_path, 'ko')

if __name__ == '__main__':
    (headers, body) = detect_intent_stream(dialog_project_id, dialog_session_id, '< audio_file_path >', 'ko')
