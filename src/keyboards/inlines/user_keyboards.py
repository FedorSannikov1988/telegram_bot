import asyncio
from loader import db
from aiogram.types import InlineKeyboardMarkup, \
                          InlineKeyboardButton
from keyboards.inlines.callback_data import navigation_items_callback


async def get_product_inline_keyboard(id: int) -> InlineKeyboardMarkup:

    product_inline_keyboard = InlineKeyboardMarkup()
    right_id = id + 1
    left_id = id - 1
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
    return product_inline_keyboard
