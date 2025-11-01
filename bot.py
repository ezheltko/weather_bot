from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from get_weather import temperature, city

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN = '8490765852:AAFHF1R7Ifm8Wl5YxWM54iO1X1qpkeTplsM'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )

@dp.message(Command(commands="pogoda"))
async def process_help_command(message: Message):
    await message.answer(f'Температура в {city} - {temperature} C')



if __name__ == '__main__':
    dp.run_polling(bot)