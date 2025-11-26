from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from config import bot_token, weather_api_key
from get_weather import get_weather_indicators

# состояние пользователей
user_data = {}

# объекты бота и деспетчера
bot = Bot(token=bot_token)
dp = Dispatcher()

# кнопки клавиатуры
geo_but = KeyboardButton(text="Отправить геолокацию", request_location=True)
city_but = KeyboardButton(text="Ввести город")
weather_but = KeyboardButton(text="Показать погоду")

# объект клавиатуры
keyboard_1 = ReplyKeyboardMarkup(keyboard=[[geo_but], [city_but], [weather_but]], resize_keyboard=True)


# обработчик команды старт
@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer("Привет!\nЯ буду присылать тебе прогноз погоды\n"
                         "Укажи свой населенный пункт", reply_markup=keyboard_1)


# обработчик команды помощь
@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer('Я буду присылать тебе прогноз погоды')


# обработчик кнопки ввести город
@dp.message(F.text == "Ввести город")
async def get_location_man(message: Message):
    await message.answer('Введи название населённого пункта', reply_markup=ReplyKeyboardRemove())


# обработчик кнопки показать погоду
@dp.message(F.text == "Показать погоду")
async def process_send_weather(message: Message):
    await message.answer(f'Температура в {get_weather_indicators(user_data[message.from_user.id], weather_api_key)}')


# обработчик кнопки "отправить геолокацию"
@dp.message(F.location)
async def process_location(message: Message):
    await message.answer(text=f'Ваши координаты: {message.location.latitude, message.location.longitude} ')
    user_data[message.from_user.id] = f"{message.location.latitude},%20{message.location.longitude}"

    print(user_data)


if __name__ == '__main__':
    dp.run_polling(bot)
