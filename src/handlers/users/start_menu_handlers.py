from keyboards import get_product_inline_keyboard, \
                      commands_start_keyboard
from aiogram.types import ReplyKeyboardRemove, \
                          InputFile
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
@dp.message_handler(text=['Инструкция'])
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


#регистрация пользователя
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


@dp.message_handler(text=['Помощь'])
async def give_all_commands_for_users(message: types.Message):
    text: str = ''
    for command, description in \
            all_answer_for_user['all_commands_for_users']['ru'].items():
        text += \
            command + ' - ' + description + '\n'
    await message.answer(text=text,
                         reply_markup=
                         commands_start_keyboard)


@dp.message_handler(text=['Скрыть меню'])
async def close_menu(message: types.Message):
    text: str = \
        all_answer_for_user['close_menu']['ru']
    await message.answer(text=text,
                         reply_markup=
                         ReplyKeyboardRemove())


@dp.message_handler(text=['Разработчик'])
async def developer_bot(message: types.Message):
    text: str = \
        all_answer_for_user['developer_contacts']['ru']
    await message.answer(text=text)


@dp.message_handler(text=['Список товаров'])
@dp.message_handler(commands=['catalog'])
async def start_looking_list_products(message: types.Message):
    first_item_info = await db.select_product_info(id=1)
    first_item_info = first_item_info[0]
    _, name, quantity, photo_path = first_item_info
    text = f"{all_answer_for_user['catalog_p1_v1']['ru']} {name}\n" \
           f"{all_answer_for_user['catalog_p2_v1']['ru']} {quantity}"

    photo = InputFile(path_or_bytesio=photo_path)

    args_for_answer_photo = {
        'photo': photo,
        'caption': text,
        'reply_markup':
            await get_product_inline_keyboard()
    }

    await message.answer_photo(**args_for_answer_photo)