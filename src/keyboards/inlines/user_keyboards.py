from loader import db
from aiogram.types import InlineKeyboardMarkup, \
                          InlineKeyboardButton
from keyboards.inlines.callback_data import navigation_items_callback


async def get_product_inline_keyboard(id: int = 1,
                                      number_purchases: int = 1) -> InlineKeyboardMarkup:

    product_info = await db.select_product_info(id=id)
    _, _, quantity_product, _ = product_info[0]

    left_id = id - 1
    right_id = id + 1

    plus_one_purchase: int = 0
    minus_one_purchase: int = 0

    if quantity_product != 0:
        plus_one_purchase = \
            number_purchases + 1
        minus_one_purchase = \
            number_purchases - 1
    else:
        plus_one_purchase, \
            number_purchases = 1, 1

    if number_purchases == 1:
        minus_one_purchase = number_purchases

    if plus_one_purchase > quantity_product:
        plus_one_purchase = quantity_product

    product_inline_keyboard = InlineKeyboardMarkup()

    if id == 1:
        btm = InlineKeyboardButton(text='>>>',
                                   callback_data=
                                   navigation_items_callback.new(
                                       number_purchases=
                                       number_purchases,
                                       for_data='products',
                                       id=right_id)
                                   )
        product_inline_keyboard.add(btm)

    elif id == await db.get_products_quantity():
        btm = InlineKeyboardButton(text='<<<',
                                   callback_data=
                                   navigation_items_callback.new(
                                       number_purchases=
                                       number_purchases,
                                       for_data='products',
                                       id=left_id)
                                   )
        product_inline_keyboard.add(btm)

    else:
        btm_left = InlineKeyboardButton(text='<<<',
                                        callback_data=
                                        navigation_items_callback.new(
                                            number_purchases=
                                            number_purchases,
                                            for_data='products',
                                            id=left_id)
                                        )

        btm_right = InlineKeyboardButton(text='>>>',
                                         callback_data=
                                         navigation_items_callback.new(
                                             number_purchases=
                                             number_purchases,
                                             for_data='products',
                                             id=right_id)
                                         )

        product_inline_keyboard.row(btm_left, btm_right)

    btm_plus = InlineKeyboardButton(text='+',
                                    callback_data=
                                    navigation_items_callback.new(
                                       number_purchases=
                                       plus_one_purchase,
                                       for_data='products',
                                       id=id)
                                   )
    btm_minus = InlineKeyboardButton(text='-',
                                     callback_data=
                                     navigation_items_callback.new(
                                         number_purchases=
                                         minus_one_purchase,
                                         for_data='products',
                                         id=id)
                                       )

    btm_quantity = InlineKeyboardButton(text=str(number_purchases),
                                        callback_data=
                                        navigation_items_callback.new(
                                            number_purchases=
                                            number_purchases,
                                            for_data='buy product',
                                            id=id)
                                        )

    btm_buy = InlineKeyboardButton(text='Купить',
                                   callback_data=
                                   navigation_items_callback.new(
                                       number_purchases=
                                       number_purchases,
                                       for_data='buy product',
                                       id=id)
                                   )

    btm_cart = InlineKeyboardButton(text='Корзина покупок',
                                    callback_data=
                                    navigation_items_callback.new(
                                        number_purchases=
                                        number_purchases,
                                        for_data='shopping cart',
                                        id=id)
                                    )

    product_inline_keyboard.row(btm_plus, btm_quantity, btm_minus)
    product_inline_keyboard.add(btm_buy)
    product_inline_keyboard.add(btm_cart)

    return product_inline_keyboard
