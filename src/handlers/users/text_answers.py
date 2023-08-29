from .commands import all_commands_for_users
from keyboards import commands_default_keyboard
from aiogram import types
from loader import dp


@dp.message_handler(text=['Клавиатура'])
async def give_start_keyboard_for_users(message: types.Message):
    text: str = 'Здраствуйте, ' \
                f'{message.from_user.first_name} '
    await message.answer(text=text,
                         reply_markup=
                         commands_default_keyboard)


@dp.message_handler(text=['Помощь'])
async def give_all_commands_for_users(message: types.Message):
    text: str = ''
    for command, description in all_commands_for_users.items():
        text += \
            command + ' - ' + description + '\n'
    await message.answer(text=text,
                         reply_markup=
                         commands_default_keyboard)


@dp.message_handler(text=['Разработчик'])
async def developer_bot(message: types.Message):
    text: str = \
        'Данного бота разработал: @Fedor_Sannikov'
    await message.answer(text=text)