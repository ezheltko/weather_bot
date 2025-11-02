from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import bot_token, weather_api_key
from get_weather import get_weather_indicators



# make bot and dispatcher objects
bot = Bot(token=bot_token)
dp = Dispatcher()


# "/start" handler
@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer('Привет!\n Я буду присылать тебе прогноз погоды')


# "/help" handler
@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer('Я буду присылать тебе прогноз погоды')
@dp.message(Command(commands="pogoda"))
async def process_help_command(message: Message):
    await message.answer(f'Температура в {get_weather_indicators('Вилейка', '8d2d07864a5d4c67a00171059250111')}')


if __name__ == '__main__':
    dp.run_polling(bot)
