from environs import Env

# create an instance of the Env class
env = Env()
# read the .env file and load variables from it into the environment
env.read_env()
# receive and save the value of the environment variable in the bot_token variable
bot_token = env('bot_token')
# receive and save the value of the environment variable in the weather_api_key variable
weather_api_key = env('weather_api_key')
