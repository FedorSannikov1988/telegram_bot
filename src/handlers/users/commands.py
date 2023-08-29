from keyboards import commands_default_keyboard
from aiogram import types
from loader import dp

all_commands_for_users: dict = \
    {
        '/start': 'начало работы ',
        '/help': 'список комманд '
                 'доступных '
                 'пользователю',
        '/manual': 'видеоинсрукция',
        '/menu': 'меню (возможности)'
                 'которые предоставляет'
                 'данный бот',
        '/developer': 'информация о '
                      'разработчике'
    }


@dp.message_handler(commands='start')
async def start_work_bot(message: types.Message):
    text: str = 'Здраствуйте, ' \
                f'{message.from_user.first_name} '
    await message.answer(text=text,
                         reply_markup=
                         commands_default_keyboard)


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
        'https://media.giphy.com/media/ThrM4jEi2lBxd7X2yz/giphy.gif'
    text: str = \
        'Пока в разработке ... ' \
        'Но я очень стараюсь:'
    await message.answer(text=text)
    await message.answer_animation(animation=
                                   url_gif_for_user)


@dp.message_handler(commands='menu')
async def menu_bot(message: types.Message):
    url_gif_for_user: str = \
        'https://media.giphy.com/media/l0K4hO8mVvq8Oygjm/giphy.gif'
    text: str = \
        'Пока в разработке ... ' \
        'Но я очень стараюсь:'
    await message.answer(text=text)
    await message.answer_animation(animation=
                                   url_gif_for_user)


@dp.message_handler(commands='developer')
async def developer_bot(message: types.Message):
    text: str = \
        'Данного бота разработал: @Fedor_Sannikov'
    await message.answer(text=text)
