from aiogram.utils.exceptions import MessageNotModified
from answers import all_urls, all_answer_for_user
from keyboards import commands_start_keyboard, \
                      navigation_items_callback, \
                      get_product_inline_keyboard
from aiogram.types import ReplyKeyboardRemove, \
                          InputMediaPhoto, \
                          InputFile
from aiogram import types
from loader import dp, db, bot
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
    text = f"Название товара: {name}\n" \
           f"Количество упаковок товара на складе: {quantity}"

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
    text = f"Название товара: {name}\n" \
           f"Количество упаковок товара на складе: {quantity}"
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
    try:
        await bot.edit_message_media(**args_for_edit_message_media)
    except MessageNotModified:
        pass
    # возможно нужно написать функцию проверяющую
    # изменилось сообщение или нет но я таким образом
    # избавился от ошибки


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

            await db.update_product_quantity(id=product_id,
                                             quantity=
                                             product_quantity-quantity_purchased_product)
        text: str = \
            f'Порядковый номер товара в каталоге: {product_id}\n' \
            f'Количество упаковок на складе: {product_quantity}\n' \
            f'Добавлено упаковок в корзину: {quantity_purchased_product}'
    else:
        text: str = \
            f'Порядковый номер товара в каталоге: {product_id}\n' \
            f'Сейчас нет в наличии. Приносим свои извинения.'

    await bot.send_message(text=text,
                           chat_id=call.message.chat.id)


#@dp.message_handler(commands=['cart'])
#@dp.message_handler(text=['Корзина покупок'])
@dp.callback_query_handler(navigation_items_callback.filter(for_data='shopping cart'))
async def view_shopping_cart(call: types.CallbackQuery):

    first_item_info = await db.select_product_info(id=1)
    first_item_info = first_item_info[0]
    _, name, quantity, photo_path = first_item_info
    text = f"Название товара: {name}\n" \
           f"Количество упаковок товара на складе: {quantity}"

    photo = InputFile(path_or_bytesio=photo_path)

    args_for_answer_photo = {
        'photo': photo,
        'caption': text,
        'reply_markup':
            await get_product_inline_keyboard()
    }

    await message.answer_photo(**args_for_answer_photo)
