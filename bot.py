from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from config import bot_token, weather_api_key
from get_weather import get_weather_indicators, city

# make bot and dispatcher objects
bot = Bot(token=bot_token)
dp = Dispatcher()

# create button objects
but_1 = KeyboardButton(text="Send location")
but_2 = KeyboardButton(text="Send location manually")

# create keyboard object
keyboard_1 = ReplyKeyboardMarkup(keyboard=[[but_1], [but_2]], resize_keyboard=True)


# "/start" handler
@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer("Привет!\n Я буду присылать тебе прогноз погоды", reply_markup=keyboard)


# "/help" handler
@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer('Я буду присылать тебе прогноз погоды')


@dp.message(Command(commands="pogoda"))
async def process_send_weather(message: Message):
    await message.answer(f'Температура в {get_weather_indicators(city, weather_api_key)}')


if __name__ == '__main__':
    dp.run_polling(bot)
