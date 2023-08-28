from aiogram import types
from loader import dp


@dp.message_handler(text=['Начать', 'Привет', 'Старт'])
@dp.message_handler(commands='start')
async def hell_func(message: types.Message):
    text: str = 'Здраствуйте, ' \
                f'{message.from_user.first_name} '
    await message.answer(text=text)


@dp.message_handler(commands=['add', 'item', 'help'])
async def hell_func(message: types.Message):
    text: str = 'Вы ввели команды: /add, /item, /help'
    await message.answer(text=text)
