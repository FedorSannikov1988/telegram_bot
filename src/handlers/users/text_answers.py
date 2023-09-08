from answers import all_urls, all_answer_for_user
from keyboards import commands_start_keyboard, \
                      navigation_items_callback, \
                      get_product_inline_keyboard
from aiogram.types import ReplyKeyboardRemove, \
                          InputMediaPhoto, \
                          InputFile
from aiogram import types
from loader import dp, db, bot


@dp.message_handler(text=['Клавиатура'])
async def give_start_keyboard_for_users(message: types.Message):
    text: str = f'{all_answer_for_user["greeting"]["ru"]}, ' \
                f'{message.from_user.first_name} '
    await message.answer(text=text,
                         reply_markup=
                         commands_start_keyboard)


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


@dp.message_handler(text=['Инструкция'])
async def manual_for_bot(message: types.Message):
    url_gif_for_user: str = \
        all_urls['manual_for_bot']

    # не помещал данную фразу в json файл
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

    # не помещал данную фразу в json файл
    text: str = \
        'Пока в разработке ... ' \
        'Но я очень стараюсь:'
    await message.answer(text=text)
    await message.answer_animation(animation=
                                   url_gif_for_user)


@dp.message_handler(text=['Список товаров'])
@dp.message_handler(commands=['catalog'])
async def start_looking_list_products(message: types.Message):
    first_item_info = await db.select_product_info(id=1)
    first_item_info = first_item_info[0]
    _, name, quantity, photo_path = first_item_info
    text = f"Название товара: {name} \n" \
           f"Количество товара: {quantity}"
    photo = InputFile(path_or_bytesio=photo_path)

    args_for_answer_photo = {
        'photo': photo,
        'caption': text,
        'reply_markup':
            await get_product_inline_keyboard(id=1)
    }

    await message.answer_photo(**args_for_answer_photo)


@dp.callback_query_handler(navigation_items_callback.filter(for_data='products'))
async def see_new_product(call: types.CallbackQuery):
    current_product_id = int(call.data.split(':')[-1])
    first_item_info = await db.select_product_info(id=current_product_id)
    first_item_info = first_item_info[0]
    _, name, count, photo_path = first_item_info
    text = f"Название товара: {name}\n" \
           f"Количество товара: {count}"
    photo = InputFile(path_or_bytesio=photo_path)

    args_for_edit_message_media = {
        'media': InputMediaPhoto(media=photo,
                                 caption=text),
        'chat_id': call.message.chat.id,
        'message_id': call.message.message_id,
        'reply_markup': await get_product_inline_keyboard(id=
                                                          current_product_id)
    }

    await bot.edit_message_media(**args_for_edit_message_media)


@dp.callback_query_handler(navigation_items_callback.filter(for_data='buy product'))
async def answer_click_button_buy(call: types.CallbackQuery):
    current_product_id = int(call.data.split(':')[-1])
    product_info = await db.select_product_info(id=
                                                current_product_id)
    product_info = product_info[0]
    product_id, _, product_quantity, _ = product_info

    if product_quantity > 0:
        user_id = call.from_user.id
        cart_user = await db.select_user_cart(user_id=
                                              user_id)

        if not cart_user:
            await db.add_purchase(user_id=user_id,
                                  purchases=product_id,
                                  number_purchases=1)
        else:
            for_dictionary_cart_user = cart_user[0]
            product_id_in_cart_user = for_dictionary_cart_user[2].split(' ')
            product_quantity_in_cart_user = for_dictionary_cart_user[3].split(' ')

            dictionary_cart_user: dict = {}
            for index_product in range(len(product_id_in_cart_user)):
                dictionary_cart_user[int(product_id_in_cart_user[index_product])] \
                    = int(product_quantity_in_cart_user[index_product])

            if product_id in dictionary_cart_user.keys():
                print(dictionary_cart_user)
                dictionary_cart_user[product_id] += 1
            else:
                dictionary_cart_user.update({product_id: 1})

            product_id_for_write = \
                ' '.join(list(map(str, dictionary_cart_user.keys())))
            product_quantity_for_write = \
                ' '.join(list(map(str, dictionary_cart_user.values())))

            await db.update_user_purchase(user_id=user_id,
                                          purchases=product_id_for_write,
                                          number_purchases=product_quantity_for_write)
            await db.update_product_quantity(id=product_id,
                                             quantity=product_quantity-1)
        text: str = \
            f'Номер товара в каталоге: {product_id}\n' \
            f'Количество упаковок на складе: {product_quantity}\n' \
            f'Одна упаковка добавлена в корзину'
    else:
        text: str = \
            f'Товара с порядковым номером: {product_id}\n' \
            f'Сейчас нет на складе\n' \
            f'Приносим свои извинения.' \

    await bot.send_message(text=text,
                           chat_id=call.message.chat.id)
