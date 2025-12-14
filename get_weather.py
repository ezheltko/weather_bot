import requests


# api: https://www.weatherapi.com/docs/
# api example: https://api.weatherapi.com/v1/astronomy.json?key=8d2d07864a5d4c67a00171059250111&q=Вилейка&aqi=no


def get_weather_indicators(town: str, key: str) -> str:
    #  функция получает данные погоды
    url = f'http://api.weatherapi.com/v1/current.json?key={key}&q={town}&aqi=no'
    # делаю запрос к api и преобразую данные в json
    weather_data = requests.get(url).json()
    location = weather_data['location']['name']
    condition = weather_data['current']['condition']['text']
    temperature = weather_data['current']['temp_c']
    humidity = weather_data['current']['humidity']
    pressure = weather_data['current']['pressure_mb']
    wind_speed = weather_data['current']['wind_kph']
    wind_direction = weather_data['current']['wind_dir']
    return (f"🌡️ Температура в {location}: {temperature}°C\n🏚️ На улице {condition}\n💧 Влажность: {humidity} %\n"
            f"🕑 Давление: {pressure} МПа\n🌬️ Скорость ветра: {wind_speed} м/с \n🧭 Направление ветра: {wind_direction}")
