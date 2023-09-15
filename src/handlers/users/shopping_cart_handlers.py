from .validation_for_delivery_questions import \
                      ValidationDeliveryQuestions
from keyboards import navigation_items_callback, \
                      navigation_cart_callback, \
                      get_shopping_cart_user
from aiogram.dispatcher import FSMContext
from answers import all_answer_for_user, \
                    all_urls
from states import DeliveryState
from loader import dp, db, bot
from aiogram import types


async def shopping_list(cart_user_text: str, cart_user: dict) -> str:
    for name_product, quantity_product in cart_user.items():
        cart_user_text += \
            name_product + ' - ' + \
            str(quantity_product) + \
            all_answer_for_user['shopping_cart_p2_v1']['ru'] + '\n'
    return cart_user_text


@dp.message_handler(commands=['test'])
async def test_middlewares(message: types.Message,
                           test_middlewares: str):
    print('test_middlewares')
    print(test_middlewares)
    await message.answer(text=
                         f'Тестируем middlewares \n'
                         f'Содержание user_baske:\n '
                         f'{test_middlewares}')


@dp.message_handler(text=['Корзина покупок', 'Shopping cart'])
@dp.message_handler(commands=['cart'])
async def view_shopping_cart(message: types.Message,
                             cart_user_info: dict[str, int]):

    cart_user_text: str = f"{all_answer_for_user['shopping_cart_p1_v1']['ru']}\n"

    if cart_user_info:
        cart_user_text = \
            await shopping_list(cart_user=cart_user_info,
                                cart_user_text=cart_user_text)

        await bot.send_message(text=cart_user_text,
                               chat_id=message.chat.id,
                               reply_markup=await get_shopping_cart_user())
    else:
        cart_user_text += all_answer_for_user['shopping_cart_p3_v1']['ru']
        await bot.send_message(text=cart_user_text,
                               chat_id=message.chat.id)


@dp.callback_query_handler(navigation_items_callback.filter(for_data=
                                                            'shopping cart'))
@dp.callback_query_handler(navigation_cart_callback.filter(operations_inside_bucket=
                                                           'shopping cart'))
async def work_with_shopping_cart(call: types.CallbackQuery,
                                  cart_user_info: dict[str, int],
                                  for_user_verification: list):

    user_id = call.from_user.id
    cart_user_text: str = f"{all_answer_for_user['shopping_cart_p1_v1']['ru']}\n"

    if 'navigation_products_btm' in call.data:


        if cart_user_info:

            cart_user_text = await shopping_list(cart_user_text=cart_user_text,
                                                 cart_user=cart_user_info)

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
        elif 'buy cart' in call.data:
            if not for_user_verification:
                cart_user_text = \
                    all_answer_for_user['shopping_cart_p4_v1']['ru']
                await bot.send_message(text=cart_user_text,
                                       chat_id=call.message.chat.id)
            elif cart_user_info:
                await bot.send_message(text=
                                       all_answer_for_user['delivery_p1_v1']['ru'],
                                       chat_id=call.message.chat.id)
                await DeliveryState.wait_data.set()
            else:
                await bot.send_message(text=
                                       all_answer_for_user['shopping_cart_p5_v1']['ru'],
                                       chat_id=call.message.chat.id)


@dp.message_handler(state=DeliveryState.wait_data)
async def get_data_for_delivery(message: types.Message, state: FSMContext):
    if ValidationDeliveryQuestions().\
            validation_data(date_string=message.text,
                            format_date="%d.%m.%Y"):
        await message.answer(text=all_answer_for_user['delivery_p2_v1']['ru'])
        await state.update_data({'data': message.text})
        await DeliveryState.wait_time.set()
    else:
        await message.answer(text=all_answer_for_user['delivery_p1_v1']['ru'])


@dp.message_handler(state=DeliveryState.wait_time)
async def get_time_for_delivery(message: types.Message, state: FSMContext):
    if ValidationDeliveryQuestions().\
            validation_time(time_string=message.text,
                            format_date="%H:%M"):
        await message.answer(text=all_answer_for_user['delivery_p3_v1']['ru'])
        await state.update_data({'time': message.text})
        await DeliveryState.wait_name_recipient_parcel.set()
    else:
        await message.answer(text=all_answer_for_user['delivery_p2_v1']['ru'])


@dp.message_handler(state=DeliveryState.wait_name_recipient_parcel)
async def get_name_for_delivery(message: types.Message, state: FSMContext):
    if ValidationDeliveryQuestions().validation_name(max_len=35,
                                                     text=message.text):
        await message.answer(text=all_answer_for_user['delivery_p4_v1']['ru'])
        await state.update_data({'name': message.text})
        await DeliveryState.wait_address.set()
    else:
        await message.answer(text=all_answer_for_user['delivery_p3_v1']['ru'])


@dp.message_handler(state=DeliveryState.wait_address)
async def get_name_for_delivery(message: types.Message,
                                state: FSMContext,
                                cart_user_info: dict[str, int]):

    await state.update_data({'address': message.text})

    data = await state.get_data()
    await state.reset_state()
    confirmation_text = f"{all_answer_for_user['delivery_p5_v1']['ru']} \n" \
                        f"{all_answer_for_user['delivery_p6_v1']['ru']} {data['data']} \n" \
                        f"{all_answer_for_user['delivery_p7_v1']['ru']} {data['time']} \n" \
                        f"{all_answer_for_user['delivery_p8_v1']['ru']} {data['name']} \n" \
                        f"{all_answer_for_user['delivery_p9_v1']['ru']} {data['address']} \n"

    cart_user_text: str = f"{all_answer_for_user['shopping_cart_p1_v1']['ru']}\n"

    cart_user_text = await shopping_list(cart_user=cart_user_info,
                                         cart_user_text=cart_user_text)

    response_user: str = confirmation_text + cart_user_text
    await message.answer(text=response_user)
    await message.answer(text=all_answer_for_user['delivery_p10_v1']['ru'])
    await message.answer_animation(animation=all_urls['delivery'])
    await message.answer(text=all_answer_for_user['delivery_p11_v1']['ru'])
    await message.answer_animation(animation=all_urls['pay'])

    user_id = message.from_user.id
    await db.delete_cart(user_id=user_id)
