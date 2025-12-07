from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import bot_token, weather_api_key
from get_weather import get_weather_indicators


# создаю главное меню
async def set_main_menu(bot: Bot):
    # создаю список команд с их описанием
    main_menu_commands = [
        BotCommand(command='help', description='Справка по работе бота'),
        BotCommand(command='/weather', description='Получить прогноз погоды'),
        BotCommand(command='/change_city', description='Изменить город'),
    ]
    await bot.set_my_commands(main_menu_commands)


# создаю класс, наследуясь от StatesGroup, в котором определяю список состояний FSM
class FSMWeatherStates(StatesGroup):
    waiting_for_city = State()
    having_city = State()


# создаю временное хранилище
storage = MemoryStorage()

# создаю словарь для хранения состояние пользователей
user_data = {}

# создаю объекты бота и диспетчера, в качестве хранилища определяю объект MemoryStorage
bot = Bot(token=bot_token)
dp = Dispatcher(storage=storage)

# создаю объекты кнопок обычной клавиатуры
geo_but = KeyboardButton(text="Отправить координаты", request_location=True)
city_but = KeyboardButton(text="Ввести город")

# создаю объекты клавиатуры
keyboard_1 = ReplyKeyboardMarkup(keyboard=[[geo_but], [city_but]], resize_keyboard=True)


# обработчик команды старт
@dp.message(Command(commands="start"), StateFilter(default_state, FSMWeatherStates.having_city))
async def process_start_command(message: Message):
    await message.answer("Я буду присылать тебе прогноз погоды\n"
                         "Укажи свой населенный пункт", reply_markup=keyboard_1)


# обработчик команды помощь
@dp.message(Command(commands="help"), StateFilter(default_state, FSMWeatherStates.having_city))
async def process_help_command(message: Message):
    await message.answer('Я буду присылать тебе прогноз погоды')


# обработчик команды погода, зная город пользователя
@dp.message(Command(commands="weather"), StateFilter(FSMWeatherStates.having_city))
async def process_send_weather(message: Message):
    await message.answer(f'{get_weather_indicators(user_data[message.from_user.id]['location'],
                                                   weather_api_key)}')


# обработчик команды погода, НЕ зная город пользователя
@dp.message(StateFilter(default_state), Command(commands="weather"))
async def process_send_weather(message: Message):
    await message.answer('Отправьте свою локацию', reply_markup=keyboard_1)


# обработчик команды изменить город
@dp.message(StateFilter(default_state, FSMWeatherStates.having_city), Command(commands="change_city"))
async def change_city(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отправьте свою локацию', reply_markup=keyboard_1)
    await state.set_state(FSMWeatherStates.waiting_for_city)


# обработчик нажатия кнопки ввести город
@dp.message(F.text == "Ввести город", StateFilter(FSMWeatherStates.waiting_for_city))
async def ask_city(message: Message, state: FSMContext):
    await message.answer('Введи название населённого пункта', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMWeatherStates.waiting_for_city)


# обработчик сообщения, содержащего название города
@dp.message(StateFilter(FSMWeatherStates.waiting_for_city))
async def get_city(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    user_data[message.from_user.id] = await state.get_data()
    await state.set_state(FSMWeatherStates.having_city)
    await message.answer(f'{get_weather_indicators(user_data[message.from_user.id]['location'],
                                                   weather_api_key)}', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMWeatherStates.having_city)
    print(user_data)


# обработчик кнопки "отправить координаты"
@dp.message(F.location)
async def process_location(message: Message, state: FSMContext):
    await state.update_data(location=f"{message.location.latitude},%20{message.location.longitude}")
    user_data[message.from_user.id] = await state.get_data()
    await message.answer(f'{get_weather_indicators(user_data[message.from_user.id]['location'],
                                                   weather_api_key)}', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMWeatherStates.having_city)
    print(user_data)


if __name__ == '__main__':
    # регистрирую функцию, которая формирует главное меню бота при запуске
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
