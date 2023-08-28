from aiogram import types

from keyboards.defoult.user_keyboards import commands_default_keyboard
from loader import dp


@dp.message_handler(text=['редис', 'помидоры', 'капуста'])
async def hell_func(message: types.Message):
    text: str = 'Это овощи !!!'
    await message.answer(text=text)


@dp.message_handler(text=['Клавиатура'])
async def hell_func(message: types.Message):
    text: str = '_'
    await message.answer(text=text,
                         reply_markup=
                         commands_default_keyboard)