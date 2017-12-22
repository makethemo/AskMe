import requests
import datetime
import json
import math

import path

with open(path.KEY_PATH, 'r') as jsonFile:  # local API key store
    key = json.load(jsonFile)

url_hourly = "http://apis.skplanetx.com/weather/current/hourly"

headers = {'Content-Type': 'application/json; charset=utf-8', 'appKey': key['weather_app_key']}

time = datetime.datetime.now().strftime('%H')  # 시스템 시간


def requestCurrentWeather(city, county, village, isHourly=True):
    params = { "version": "1",
                "city": city,
                "county": county,
                "village": village }
    if isHourly:
        response = requests.get(url_hourly, params=params, headers=headers)

    if response.status_code == 200:
        response_body = response.json()

        if isHourly:  # 날씨 정보
            weather_data = response_body['weather']['hourly'][0]
            return hourly(weather_data)
    else:
        return  # 에러


def hourly(weather):  # 현재 날씨(시간별)
    temperature_tmax = weather['temperature']['tmax']  # 오늘의 최고기온
    temperature_tc = weather['temperature']['tc']  # 1시간 현재기온
    temperature_tmin = weather['temperature']['tmin']  # 오늘의 최저기온
    sky_name = weather['sky']['name']  # 하늘상태

    result = time + '시 기준으로 온도는 ' + temperature_tc + '도 이고, 최고 ' + temperature_tmax + '도, 최저' + temperature_tmin + '도, 하늘상태는 ' + sky_name + '입니다.'
    return result


if __name__ == '__main__':
    # requestCurrentWeather('city', 'county', 'village')
    print(requestCurrentWeather('서울', '강남구', '논현동'))
