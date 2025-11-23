from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from config import bot_token, weather_api_key
from get_weather import get_weather_indicators

# dict for user data
user_data = {}

# make bot and dispatcher objects
bot = Bot(token=bot_token)
dp = Dispatcher()

# create button objects
but_1 = KeyboardButton(text="Отправить локацию автоматически")
but_2 = KeyboardButton(text="Ввести локацию вручную")

# create keyboard object
keyboard_1 = ReplyKeyboardMarkup(keyboard=[[but_1], [but_2]], resize_keyboard=True)


# start handler
@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer("Привет!\n Я буду присылать тебе прогноз погоды", reply_markup=keyboard_1)


# help handler
@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer('Я буду присылать тебе прогноз погоды')


# send location manually handler
@dp.message(F.text == "Ввести локацию вручную")
async def get_location_man(message: Message):
    await message.answer('Введите название вашего населённого пункта', reply_markup=ReplyKeyboardRemove())


@dp.message(Command(commands="pogoda"))
async def process_send_weather(message: Message):
    await message.answer(f'Температура в {get_weather_indicators(user_data['location'], weather_api_key)}')


@dp.message()
async def get_location_man(message: Message):
    await message.answer(text=f'Ты будешь получать погоду для {message.text}')
    user_data['location'] = message.text


if __name__ == '__main__':
    dp.run_polling(bot)
