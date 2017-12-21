import dialogflow
from camera import camera
from vision import vision_api_request
from search import dictionary


def detect_intent_stream(project_id, session_id, audio_file_path, language_code):

    session_client = dialogflow.SessionsClient()
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    def request_generator(audio_config, audio_file_path):
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session, query_input=query_input)

        with open(audio_file_path, 'rb') as audio_file:
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

    if intent_name == "picture":
        camera.take_a_picture()

    if intent_name == "what":
        picture = camera.take_a_picture()  # 사진 찍기
        labels = vision_api_request.get_label(picture)  # vision에 사진 전송
        # TODO labels list를 문장화 시켜서 리턴.

    if intent_name == "search":
        return dictionary.search_keyword_by_naver_dic(query_result.fulfillment_text)

    if intent_name == "weather":
        pass

    return intent_name


if __name__ == '__main__':
    detect_intent_stream('< project_id >', '< client_access_token >', '< audio_file_path >', '< language_code >')
