from aiogram.utils.exceptions import MessageNotModified
from answers import all_urls, all_answer_for_user
from keyboards import commands_start_keyboard, \
                      navigation_items_callback, \
                      get_product_inline_keyboard, \
                      get_shopping_cart_user
from aiogram.types import ReplyKeyboardRemove, \
                          InputMediaPhoto, \
                          InputFile
from loader import dp, db, bot
from aiogram import types
import json


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


@dp.callback_query_handler(navigation_items_callback.filter(for_data='products'))
async def see_new_product_in_catalog(call: types.CallbackQuery):
    current_product_id = int(call.data.split(':')[-2])
    quantity_purchased_product = int(call.data.split(':')[-1])
    first_item_info = await db.select_product_info(id=current_product_id)
    _, name, quantity, photo_path = first_item_info[0]
    text = f"{all_answer_for_user['catalog_p1_v1']['ru']} {name}\n" \
           f"{all_answer_for_user['catalog_p2_v1']['ru']} {quantity}"
    photo = InputFile(path_or_bytesio=photo_path)

    args_for_edit_message_media = {
        'media': InputMediaPhoto(media=photo,
                                 caption=text),
        'chat_id': call.message.chat.id,
        'message_id': call.message.message_id,
        'reply_markup':
            await get_product_inline_keyboard(
                id=current_product_id,
                number_purchases=
                quantity_purchased_product
            )
    }
    # возможно нужно написать функцию проверяющую
    # изменилось сообщение или нет но я таким образом
    # избавился от ошибки
    try:
        await bot.edit_message_media(**args_for_edit_message_media)
    except MessageNotModified:
        pass


@dp.callback_query_handler(navigation_items_callback.filter(for_data='buy product'))
async def answer_click_button_buy(call: types.CallbackQuery):
    current_product_id = int(call.data.split(':')[-2])
    quantity_purchased_product = int(call.data.split(':')[-1])
    product_info = await db.select_product_info(id=
                                                current_product_id)
    product_id, _, product_quantity, _ = product_info[0]

    if product_quantity > 0:
        user_id = call.from_user.id
        cart_user = await db.select_user_cart(user_id=
                                              user_id)

        user_shopping_cart: dict = {}

        if not cart_user:
            user_shopping_cart = {product_id: quantity_purchased_product}

            await db.add_purchase(user_id=user_id,
                                  purchases=
                                  json.dumps(user_shopping_cart))
        else:
            user_shopping_cart = json.loads(cart_user[0][2])

            product_id_str = str(product_id)
            if product_id_str in user_shopping_cart.keys():
                user_shopping_cart[product_id_str] += quantity_purchased_product
            else:
                user_shopping_cart.update({product_id: quantity_purchased_product})

            await db.update_user_purchase(user_id=user_id,
                                          purchases=
                                          json.dumps(user_shopping_cart))
            new_product_quantity = \
                product_quantity - quantity_purchased_product
            await db.update_product_quantity(id=product_id,
                                             quantity=
                                             new_product_quantity)
        text: str = \
            f"{all_answer_for_user['catalog_p1_v2']['ru']} {product_id}\n" \
            f"{all_answer_for_user['catalog_p2_v2']['ru']} {product_quantity}\n" \
            f"{all_answer_for_user['catalog_p3_v2']['ru']} {quantity_purchased_product}"
    else:
        text: str = \
            f"{all_answer_for_user['catalog_p1_v2']['ru']} {product_id}\n" \
            f"{all_answer_for_user['catalog_p4_v2']['ru']}"

    await bot.send_message(text=text,
                           chat_id=call.message.chat.id)


@dp.callback_query_handler(navigation_items_callback.filter(for_data='shopping cart'))
async def view_shopping_cart(call: types.CallbackQuery):
    for_buy_cart = call.data.split(':')[-1]
    for_delete_cart = call.data.split(':')[-2]
    user_id = call.from_user.id
    cart_user_text: str = f"{all_answer_for_user['shopping_cart_p1_v1']['ru']}\n"
    if for_buy_cart == '1':
        cart_user = await db.select_user_cart(user_id=user_id)

        if cart_user:
            cart_user: dict = json.loads(cart_user[0][2])

            for id_product, quantity_product in cart_user.items():
                for_name_product = await db.select_product_info(id=id_product)
                name_product = for_name_product[0][1]
                cart_user_text += \
                    name_product + ' - ' + \
                    str(quantity_product) + \
                    all_answer_for_user['shopping_cart_p2_v1']['ru'] + \
                    '\n'

            await bot.send_message(text=cart_user_text,
                                   chat_id=call.message.chat.id,
                                   reply_markup=await get_shopping_cart_user())
        else:
            cart_user_text += all_answer_for_user['shopping_cart_p3_v1']['ru']
            await bot.send_message(text=cart_user_text,
                                   chat_id=call.message.chat.id)

    elif for_delete_cart == 'True':
        cart_user_text += \
            all_answer_for_user['shopping_cart_p3_v1']['ru']
        await db.delete_cart(user_id=user_id)
        await bot.send_message(text=cart_user_text,
                               chat_id=call.message.chat.id)

    elif for_buy_cart == 'True':
        for_user_verification = await db.select_user_info(id=user_id)
        if not for_user_verification:
            cart_user_text = \
                all_answer_for_user['shopping_cart_p4_v1']['ru']
            await bot.send_message(text=cart_user_text,
                                   chat_id=call.message.chat.id)
        else:
            await bot.send_animation(
                chat_id=call.message.chat.id,
                animation=all_urls['pay'])


@dp.message_handler(text=['Корзина покупок'])
@dp.message_handler(commands=['cart'])
async def view_shopping_cart(message: types.Message):

    user_id = message.from_user.id
    cart_user_text: str = f"{all_answer_for_user['shopping_cart_p1_v1']['ru']}\n"

    cart_user = await db.select_user_cart(user_id=user_id)

    if cart_user:
        cart_user: dict = json.loads(cart_user[0][2])

        for id_product, quantity_product in cart_user.items():
            for_name_product = await db.select_product_info(id=id_product)
            name_product = for_name_product[0][1]
            cart_user_text += \
                name_product + ' - ' + \
                str(quantity_product) + \
                all_answer_for_user['shopping_cart_p2_v1']['ru'] + '\n'

        await bot.send_message(text=cart_user_text,
                               chat_id=message.chat.id,
                               reply_markup=await get_shopping_cart_user())
    else:
        cart_user_text += all_answer_for_user['shopping_cart_p3_v1']['ru']
        await bot.send_message(text=cart_user_text,
                               chat_id=message.chat.id)
