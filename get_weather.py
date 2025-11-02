import requests

# api: https://www.weatherapi.com/docs/

city = 'Вилейка'



def get_weather_indicators(town: str, key: str) -> tuple:
    #  get the weather indicators
    url = f'http://api.weatherapi.com/v1/current.json?key={key}&q={town}&aqi=no'
    # make request to api and get weather_data in json
    weather_data = requests.get(url).json()
    location = weather_data['location']['name']
    condition = weather_data['current']['condition']['text']
    temperature = weather_data['current']['temp_c']
    humidity = weather_data['current']['humidity']
    pressure = weather_data['current']['pressure_mb']
    wind_speed = weather_data['current']['wind_kph']
    wind_direction = weather_data['current']['wind_dir']
    return location, condition, temperature, humidity, pressure, wind_speed, wind_direction


