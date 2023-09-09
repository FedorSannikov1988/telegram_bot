from aiogram.types import ReplyKeyboardMarkup, \
                          KeyboardButton
from answers import button_names

commands_start_keyboard = \
    ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_names['help']['ru']),
                KeyboardButton(text=button_names['instruction']['ru'])
            ],
            [
                KeyboardButton(text=button_names['list_products']['ru']),
                KeyboardButton(text=button_names['cart']['ru']),
                KeyboardButton(text=button_names['registration']['ru'],
                               request_contact=True),
            ],
            [
                KeyboardButton(text=button_names['developer']['ru']),
                KeyboardButton(text=button_names['hide_menu']['ru'])
            ]
        ],
        resize_keyboard=True
)