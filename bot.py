from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext

from config import bot_token, weather_api_key
from get_weather import get_weather_indicators


# создаю список состояний FSM
class FSMWeatherStates(StatesGroup):
    waiting_for_city = State()
    having_city = State()


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
keyboard_1 = ReplyKeyboardMarkup(keyboard=[[geo_but], [city_but]], resize_keyboard=True)
keyboard_2 = ReplyKeyboardMarkup(keyboard=[[weather_but]])


# обработчик команды старт
@dp.message(Command(commands="start"), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer("Привет!\nЯ буду присылать тебе прогноз погоды\n"
                         "Укажи свой населенный пункт", reply_markup=keyboard_1)


# обработчик команды помощь
@dp.message(Command(commands="help"), StateFilter(default_state, FSMWeatherStates.having_city))
async def process_help_command(message: Message):
    await message.answer('Я буду присылать тебе прогноз погоды')


# обработчик нажатия кнопки ввести город
@dp.message(F.text == "Ввести город", StateFilter(default_state))
async def ask_city(message: Message, state: FSMContext):
    await message.answer('Введи название населённого пункта', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMWeatherStates.waiting_for_city)


# обработчик ввода города
@dp.message(StateFilter(FSMWeatherStates.waiting_for_city))
async def get_city(message: Message, state: FSMContext):
    user_data[message.from_user.id] = message.text.strip()
    await state.set_state(FSMWeatherStates.having_city)
    await message.answer(f'Температура в {get_weather_indicators(user_data[message.from_user.id], weather_api_key)}')


# обработчик кнопки показать погоду, зная город пользователя
@dp.message(Command(commands="weather"), StateFilter(FSMWeatherStates.having_city))
@dp.message(F.text == "Показать погоду", StateFilter(FSMWeatherStates.having_city))
async def process_send_weather(message: Message):
    await message.answer(f'Температура в {get_weather_indicators(user_data[message.from_user.id], weather_api_key)}')


# обработчик кнопки показать погоду, НЕ зная город пользователя
@dp.message(StateFilter(default_state), Command(commands="weather"))
@dp.message(StateFilter(default_state), F.text == "Показать погоду")
async def process_send_weather(message: Message):
    await message.answer('Отправте свою локацию', reply_markup=keyboard_1)


# обработчик кнопки "отправить геолокацию"
@dp.message(F.location)
async def process_location(message: Message):
    await message.answer(text=f'Ваши координаты: {message.location.latitude, message.location.longitude} ')
    user_data[message.from_user.id] = f"{message.location.latitude},%20{message.location.longitude}"
    await message.answer(f'Температура в {get_weather_indicators(user_data[message.from_user.id], weather_api_key)}')

    print(user_data)


if __name__ == '__main__':
    dp.run_polling(bot)
