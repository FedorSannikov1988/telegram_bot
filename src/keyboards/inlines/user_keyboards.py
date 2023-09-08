from loader import db
from aiogram.types import InlineKeyboardMarkup, \
                          InlineKeyboardButton
from keyboards.inlines.callback_data import navigation_items_callback


async def get_product_inline_keyboard(id: int) -> InlineKeyboardMarkup:

    left_id = id - 1
    right_id = id + 1
    product_inline_keyboard = InlineKeyboardMarkup()

    if id == 1:
        btm = InlineKeyboardButton(text='>>>',
                                   callback_data=
                                   navigation_items_callback.new(
                                       for_data='products',
                                       id=right_id)
                                   )
        product_inline_keyboard.add(btm)

    elif id == await db.get_products_quantity():
        btm = InlineKeyboardButton(text='<<<',
                                   callback_data=
                                   navigation_items_callback.new(
                                       for_data='products',
                                       id=left_id)
                                   )
        product_inline_keyboard.add(btm)

    else:
        btm_left = InlineKeyboardButton(text='<<<',
                                        callback_data=
                                        navigation_items_callback.new(
                                            for_data='products',
                                            id=left_id)
                                        )

        btm_right = InlineKeyboardButton(text='>>>',
                                         callback_data=
                                         navigation_items_callback.new(
                                             for_data='products',
                                             id=right_id)
                                         )

        product_inline_keyboard.row(btm_left, btm_right)

    btm_buy = InlineKeyboardButton(text='Купить',
                                   callback_data=
                                   navigation_items_callback.new(
                                       for_data='buy product',
                                       id=id)
                                   )

    btm_cart = InlineKeyboardButton(text='Корзина покупок',
                                    callback_data=
                                    navigation_items_callback.new(
                                        for_data='shopping cart',
                                        id=id)
                                    )

    product_inline_keyboard.add(btm_buy)
    product_inline_keyboard.add(btm_cart)

    return product_inline_keyboard
