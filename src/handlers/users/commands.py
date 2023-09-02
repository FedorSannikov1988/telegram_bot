from answers import all_answer_for_user, all_urls
from keyboards import commands_start_keyboard
from aiogram import types
from loader import dp
from loader import db


all_commands_for_users: dict = \
    all_answer_for_user['all_commands_for_users']['ru']


@dp.message_handler(commands='start')
async def start_work_bot(message: types.Message):
    text: str = 'Здраствуйте, ' \
                f'{message.from_user.first_name} '
    await message.answer(text=text,
                         reply_markup=
                         commands_start_keyboard)


@dp.message_handler(commands='help')
async def give_all_commands_for_users(message: types.Message):
    text: str = ''
    for command, description in all_commands_for_users.items():
        text += \
            command + ' - ' + description + '\n'
    await message.answer(text=text)


@dp.message_handler(commands='manual')
async def manual_for_bot(message: types.Message):
    url_gif_for_user: str = \
        all_urls['manual_for_bot']

    text: str = \
        'Пока в разработке ... ' \
        'Но я очень стараюсь:'
    await message.answer(text=text)
    await message.answer_animation(animation=
                                   url_gif_for_user)


@dp.message_handler(commands='menu')
async def menu_bot(message: types.Message):
    url_gif_for_user: str = \
        all_urls['menu_bot']

    text: str = \
        'Пока в разработке ... ' \
        'Но я очень стараюсь:'
    await message.answer(text=text)
    await message.answer_animation(animation=
                                   url_gif_for_user)


@dp.message_handler(content_types=['contact'])
async def get_contact_users(message: types.Message):
    if message.contact.user_id == message.from_user.id:
        text: str = 'Регистрация пройдена'
        await message.answer(text=text)
        db.add_user(int(message.from_user.id),
                    str(message.contact.phone_number))
    else:
        text: str = 'Регистрация НЕ пройдена'
        await message.answer(text=text)
