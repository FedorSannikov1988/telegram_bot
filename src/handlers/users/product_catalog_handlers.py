"""
Product Catalog
"""
from aiogram.utils.exceptions import MessageNotModified
from keyboards import get_product_inline_keyboard,\
                      navigation_items_callback
from aiogram.types import InputMediaPhoto, \
                          InputFile
from answers import all_answer_for_user
from loader import dp, db, bot
from aiogram import types
from loader import logger
import json


@dp.callback_query_handler(navigation_items_callback.filter(for_data='products'))
async def see_new_product_in_catalog(call: types.CallbackQuery, product_info: list):
    """
    Scrolling the catalog by the user

    :param call: types.CallbackQuery
    :param product_info: list
    :return: None
    """
    current_product_id = int(call.data.split(':')[-2])
    quantity_purchased_product = int(call.data.split(':')[-1])
    _, name, quantity, photo_path = product_info[0]

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

    try:
        await bot.edit_message_media(**args_for_edit_message_media)
    except MessageNotModified as small_problem_caused_update:
        logger.warning(small_problem_caused_update)


@dp.callback_query_handler(navigation_items_callback.filter(for_data='buy product'))
async def answer_click_button_buy(call: types.CallbackQuery, product_info: list):
    """
    Reaction when the buy button is clicked.

    :param call: types.CallbackQuery
    :param product_info: list
    :return: None
    """

    quantity_purchased_product = int(call.data.split(':')[-1])
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
            f"{all_answer_for_user['catalog_p1_v2']['ru']}\n {product_id}\n" \
            f"{all_answer_for_user['catalog_p2_v2']['ru']} {product_quantity}\n" \
            f"{all_answer_for_user['catalog_p3_v2']['ru']} {quantity_purchased_product}"
    else:
        text: str = \
            f"{all_answer_for_user['catalog_p1_v2']['ru']} {product_id}\n" \
            f"{all_answer_for_user['catalog_p4_v2']['ru']}"

    #await bot.send_message(text=text,
    #                       chat_id=call.message.chat.id,
    #                       disable_notification=True)
    #await bot.answer_callback_query(callback_query_id=call.id,
    #                                text=text)

    await bot.answer_callback_query(callback_query_id=call.id,
                                    text=text,
                                    show_alert=True)