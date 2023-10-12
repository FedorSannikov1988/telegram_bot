"""
Getting started with the bot (main menu)
"""
from aiogram.utils.markdown import hstrikethrough, \
                                   hunderline, \
                                   hitalic, \
                                   hlink, \
                                   hbold
from keyboards import get_product_inline_keyboard, \
                      commands_start_keyboard
from aiogram.types import ReplyKeyboardRemove, \
                          InputFile
from aiogram.dispatcher import FSMContext
from answers import all_answer_for_user, \
                    all_urls
from states import QuestionnaireState
from aiogram import types
from loader import dp, db


@dp.message_handler(commands=['start'])
async def start_work_bot(message: types.Message):
    """
    Reaction to the start command.

    :param message: types.Message
    :return: None
    """
    text: str = f'{all_answer_for_user["greeting"]["ru"]}, ' \
                f'{hbold(message.from_user.first_name)} \n' \
                f'Я - {hstrikethrough("БОЕВОЙ")} 🏹🪖⚔️ ' \
                f'{hitalic("УЧЕБНЫЙ ПРОЕКТ")} 👨🏻‍🎓 ! \n' \
                f'{hunderline("Будем делать покупки: ")} ' \
                f'🍅, 🍆, 🥔, 🥕, 🥒, 🫑 для ' \
                f'🥗 {hunderline("вместе.")}\n' \
                f'Мой ➡️ ' \
                f'{hlink( url= r"https://t.me/Fedor_Sannikov", title="создатель")}.'
    await message.answer(text=text,
                         reply_markup=
                         commands_start_keyboard)


@dp.message_handler(commands=['help'])
async def give_all_commands_for_users(message: types.Message):
    """
    Reaction to the help command.

    :param message: types.Message
    :return: None
    """
    text: str = ''
    for command, description in \
            all_answer_for_user['all_commands_for_users']['ru'].\
                                                         items():
        text += \
            command + ' - ' + description + '\n'
    await message.answer(text=text)


@dp.message_handler(commands=['manual'])
@dp.message_handler(text=['Инструкция', 'Instruction'])
async def manual_for_bot(message: types.Message):
    """
    Reaction to the manual command.

    :param message: types.Message
    :return: None
    """
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
async def get_contact_users(message: types.Message,
                            contact_user_id: int,
                            contact_user_phone: str,
                            search_results_user: list):
    """
    User Registration

    :param message: types.Message
    :param contact_user_id: int
    :param contact_user_phone: str
    :param search_results_user: list
    :return: None
    """
    if message.contact.user_id == message.from_user.id:

        if not search_results_user:

            text: str = \
                all_answer_for_user['registration_positive']['ru']

            await db.add_user(id=contact_user_id,
                              phone=contact_user_phone)

        elif search_results_user:

            text: str = \
                all_answer_for_user['registration_user_exists']['ru']

        else:
            text: str = \
                all_answer_for_user['registration_negative']['ru']

        await message.answer(text=text)


@dp.message_handler(text=['Помощь', 'Help'])
async def give_all_commands_for_users(message: types.Message):
    """
    Output of all bot commands.

    :param message: types.Message
    :return: None
    """

    text: str = ''
    for command, description in \
            all_answer_for_user['all_commands_for_users']['ru'].items():
        text += \
            command + ' - ' + description + '\n'
    await message.answer(text=text,
                         reply_markup=
                         commands_start_keyboard)


@dp.message_handler(text=['Скрыть меню', 'Hide menu'])
async def close_menu(message: types.Message):
    """
    Reaction to the text "Hide menu".

    :param message: types.Message
    :return: None
    """
    text: str = \
        all_answer_for_user['close_menu']['ru']
    await message.answer(text=text,
                         reply_markup=
                         ReplyKeyboardRemove())


@dp.message_handler(text=['Разработчик', 'Developer'])
async def developer_bot(message: types.Message):
    """
    Says who developed the bot.

    :param message: types.Message
    :return: None
    """
    text: str = \
        all_answer_for_user['developer_contacts']['ru']
    await message.answer(text=text)


@dp.message_handler(text=['Список товаров', 'List products'])
@dp.message_handler(commands=['catalog'])
async def start_looking_list_products(message: types.Message,
                                      first_product_info: tuple):
    """
    Starting the Product catalog view

    :param message:
    :param first_product_info:
    :return: None
    """
    _, name, quantity, photo_path = first_product_info
    text = \
        f"{all_answer_for_user['catalog_p1_v1']['ru']} {name}\n" \
        f"{all_answer_for_user['catalog_p2_v1']['ru']} {quantity}"

    photo = InputFile(path_or_bytesio=photo_path)

    args_for_answer_photo = {
        'photo': photo,
        'caption': text,
        'reply_markup':
            await get_product_inline_keyboard()
    }
    await message.answer_photo(**args_for_answer_photo)


@dp.message_handler(text=['Анкетирование', 'Survey'])
@dp.message_handler(commands=['ankete'])
async def start_ankete(message: types.Message):
    """
    Launching a questionnaire for the buyer.

    :param message: types.Message
    :return: None
    """
    text = all_answer_for_user['ankete_number_questions']['ru'] + '\n' + \
           all_answer_for_user['ankete_q1']['ru']
    await message.answer(text=text)
    await QuestionnaireState.wait_what_like.set()


@dp.message_handler(state=QuestionnaireState.wait_what_like)
async def get_not_like_store(message: types.Message, state: FSMContext):
    """
    The answer to the question what the customer
    does not like in the store

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    await state.update_data({'not_like': message.text})
    text = all_answer_for_user['ankete_q2']['ru']
    await message.answer(text=text)
    await QuestionnaireState.wait_announcement_results.set()


@dp.message_handler(state=QuestionnaireState.wait_announcement_results)
async def get_like_store(message: types.Message, state: FSMContext):
    """
    The answer to the question what does the customer like in the store

    :param message: FSMContext
    :param state: FSMContext
    :return: None
    """
    await state.update_data({'like': message.text})

    data = await state.get_data()
    await state.reset_state()

    results_text = f"{all_answer_for_user['ankete_resalt']['ru']} " \
                   f"пользователя {message.from_user.first_name} \n" \
                   f"{all_answer_for_user['ankete_q1']['ru']} \n" \
                   f"{data['not_like']} \n" \
                   f"{all_answer_for_user['ankete_q2']['ru']} \n" \
                   f"{data['like']} \n"
    await message.answer(text=results_text)
