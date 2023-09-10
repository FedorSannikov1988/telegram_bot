from answers import all_urls, all_answer_for_user
from keyboards import navigation_items_callback, \
                      navigation_cart_callback, \
                      get_shopping_cart_user
from states import DeliveryState
from loader import dp, db, bot
from aiogram import types
import json


@dp.callback_query_handler(navigation_items_callback.filter(for_data=
                                                            'shopping cart'))
@dp.callback_query_handler(navigation_cart_callback.filter(operations_inside_bucket=
                                                           'shopping cart'))
async def view_shopping_cart(call: types.CallbackQuery):

    user_id = call.from_user.id
    cart_user_text: str = f"{all_answer_for_user['shopping_cart_p1_v1']['ru']}\n"

    if 'navigation_products_btm' in call.data:
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
    else:
        if 'delete cart' in call.data:
            cart_user_text += \
                all_answer_for_user['shopping_cart_p3_v1']['ru']
            await db.delete_cart(user_id=user_id)
            await bot.send_message(text=cart_user_text,
                                   chat_id=call.message.chat.id)
        # можно заменить на else:
        # но хочется что бы ветка собыий
        # явно показывала куда она идет
        elif 'buy cart' in call.data:
            for_user_verification = await db.select_user_info(id=user_id)
            if not for_user_verification:
                cart_user_text = \
                    all_answer_for_user['shopping_cart_p4_v1']['ru']
                await bot.send_message(text=cart_user_text,
                                       chat_id=call.message.chat.id)
            else:
                await bot.send_message(text='Укажите дату доставки товара в формате дд.мм.гггг',
                                       chat_id=call.message.chat.id)
                await DeliveryState.wait_data.set()

                #await bot.send_animation(
                #    chat_id=call.message.chat.id,
                #    animation=all_urls['pay'])


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
