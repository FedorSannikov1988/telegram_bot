from keyboards import commands_start_keyboard
from answers import all_answer_for_user, \
                    all_urls
from aiogram import types
from loader import dp, db


@dp.message_handler(commands=['start'])
async def start_work_bot(message: types.Message):
    text: str = f'{all_answer_for_user["greeting"]["ru"]}, ' \
                f'{message.from_user.first_name} '
    await message.answer(text=text,
                         reply_markup=
                         commands_start_keyboard)


@dp.message_handler(commands=['help'])
async def give_all_commands_for_users(message: types.Message):
    text: str = ''
    for command, description in \
            all_answer_for_user['all_commands_for_users']['ru'].\
                                                         items():
        text += \
            command + ' - ' + description + '\n'
    await message.answer(text=text)


@dp.message_handler(commands=['manual'])
async def manual_for_bot(message: types.Message):
    url_gif_for_user: str = \
        all_urls['manual_for_bot']

    #не помещал данную фразу в json файл
    text: str = \
        'Пока в разработке ... ' \
        'Но я очень стараюсь:'
    await message.answer(text=text)
    await message.answer_animation(animation=
                                   url_gif_for_user)


@dp.message_handler(content_types=['contact'])
async def get_contact_users(message: types.Message):

    if message.contact.user_id == message.from_user.id:

        user_id: int = int(message.from_user.id)
        user_phone: str = str(message.contact.phone_number)
        search_results_user = await db.select_user_info(id=user_id,
                                                        phone=user_phone)

        if search_results_user:
            search_results_user = search_results_user[0]

        if not (user_id in search_results_user) or \
           not (user_phone in search_results_user):

            await db.add_user(id=user_id, phone=user_phone)
            text: str = \
                all_answer_for_user['registration_positive']['ru']
        else:
            text: str = \
                all_answer_for_user['registration_user_exists']['ru']
        await message.answer(text=text)
    else:
        text: str = \
            all_answer_for_user['registration_negative']['ru']
        await message.answer(text=text)
