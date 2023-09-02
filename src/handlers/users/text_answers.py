from keyboards import commands_start_keyboard
from aiogram.types import ReplyKeyboardRemove
# вероятно не очень хорошо что я подгружаю из
# соседнего модуля но с другой стороны зачем
# грузить и замет обрабатывать из from answers
# если это сделано в .commands
from .commands import all_commands_for_users
from answers import all_urls
from aiogram import types
from loader import dp


@dp.message_handler(text=['Клавиатура'])
async def give_start_keyboard_for_users(message: types.Message):
    text: str = 'Здраствуйте, ' \
                f'{message.from_user.first_name} '
    await message.answer(text=text,
                         reply_markup=
                         commands_start_keyboard)


@dp.message_handler(text=['Помощь'])
async def give_all_commands_for_users(message: types.Message):
    text: str = ''
    for command, description in all_commands_for_users.items():
        text += \
            command + ' - ' + description + '\n'
    await message.answer(text=text,
                         reply_markup=
                         commands_start_keyboard)


@dp.message_handler(text=['Скрыть меню'])
async def close_menu(message: types.Message):
    await message.answer(text='Для вызова меню введите комманду: /start',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=['Разработчик'])
async def developer_bot(message: types.Message):
    text: str = \
        'Данного бота разработал: @Fedor_Sannikov'
    await message.answer(text=text)


@dp.message_handler(text=['Инструкция'])
async def manual_for_bot(message: types.Message):
    url_gif_for_user: str = \
        all_urls['manual_for_bot']

    print(url_gif_for_user)

    text: str = \
        'Пока в разработке ... ' \
        'Но я очень стараюсь:'
    await message.answer(text=text)
    await message.answer_animation(animation=
                                   url_gif_for_user)


@dp.message_handler(text=['Меню'])
async def menu_bot(message: types.Message):
    url_gif_for_user: str = \
        all_urls['menu_bot']

    text: str = \
        'Пока в разработке ... ' \
        'Но я очень стараюсь:'
    await message.answer(text=text)
    await message.answer_animation(animation=
                                   url_gif_for_user)
