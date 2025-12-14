from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, BotCommand
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import bot_token, weather_api_key
from get_weather import get_weather_indicators


# создаю класс, наследуясь от StatesGroup, в котором определяю список состояний FSM
class FSMWeatherStates(StatesGroup):
    waiting_for_city = State()
    waiting_for_location = State()
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
keyboard_set_location = ReplyKeyboardMarkup(keyboard=[[geo_but], [city_but]], resize_keyboard=True)


# создаю главное меню
async def set_main_menu(bot: Bot):
    # создаю список команд с их описанием
    main_menu_commands = [
        BotCommand(command='help', description='Справка по работе бота'),
        BotCommand(command='weather', description='Получить прогноз погоды'),
        BotCommand(command='change_city', description='Изменить город'),
    ]
    await bot.set_my_commands(main_menu_commands)


# обработчик команды START
@dp.message(Command(commands="start"))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer("Я буду присылать тебе прогноз погоды\n"
                         "Укажи свой населенный пункт", reply_markup=keyboard_set_location)
    await state.set_state(FSMWeatherStates.waiting_for_city)


# обработчик команды HELP
@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer('Я буду присылать тебе прогноз погоды')


# обработчик команды WEATHER, зная город пользователя
@dp.message(Command(commands="weather"), StateFilter(FSMWeatherStates.having_city))
async def process_send_weather(message: Message):
    await message.answer(f'{get_weather_indicators(user_data[message.from_user.id]['location'],
                                                   weather_api_key)}')


# обработчик команды WEATHER, НЕ зная город пользователя
@dp.message(Command(commands="weather"))
async def process_send_weather(message: Message):
    await message.answer('Отправь свою локацию', reply_markup=keyboard_set_location)


# обработчик команды CHANGE_CITY
@dp.message(StateFilter(FSMWeatherStates.having_city), Command(commands="change_city"))
async def change_city(message: Message, state: FSMContext):
    await message.answer('Отправьте свою локацию', reply_markup=keyboard_set_location)
    await state.set_state(FSMWeatherStates.waiting_for_city)


# обработчик нажатия кнопки "ВВЕСТИ ГОРОД"
@dp.message(F.text == "Ввести город", StateFilter(FSMWeatherStates.waiting_for_city))
async def ask_city(message: Message, state: FSMContext):
    print(message.model_dump_json())
    await message.answer('Введи название населённого пункта', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMWeatherStates.waiting_for_city)


# обработчик нажатия кнопки "ОТПРАВИТЬ КООРДИНАТЫ" и сообщения, содержащего название города
@dp.message(StateFilter(FSMWeatherStates.waiting_for_city))
@dp.message(F.location, StateFilter(FSMWeatherStates.waiting_for_city))
async def process_location(message: Message, state: FSMContext):
    if message.location:
        print(message.model_dump_json())
        await state.update_data(location=f"{message.location.latitude},%20{message.location.longitude}")
        user_data[message.from_user.id] = await state.get_data()
        await message.answer(f'{get_weather_indicators(user_data[message.from_user.id]['location'],
                                                       weather_api_key)}', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSMWeatherStates.having_city)
    elif message.text:
        await state.update_data(location=message.text)
        user_data[message.from_user.id] = await state.get_data()
        await state.set_state(FSMWeatherStates.having_city)
        await message.answer(f'{get_weather_indicators(user_data[message.from_user.id]['location'],
                                                       weather_api_key)}', reply_markup=ReplyKeyboardRemove())
        await state.set_state(FSMWeatherStates.having_city)
    print(user_data)


if __name__ == '__main__':
    # регистрирую функцию, которая формирует главное меню бота при запуске
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
