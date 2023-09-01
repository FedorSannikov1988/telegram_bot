from aiogram.types import ReplyKeyboardMarkup, \
                          KeyboardButton

commands_default_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/help')
        ],
        [
            KeyboardButton(text='/manual')
        ],
        [
            KeyboardButton(text='/menu')
        ],
        [
            KeyboardButton(text='/developer')
        ],
        [
            KeyboardButton(text='Добавить номер телефона',
                           request_contact=True)
        ]
    ],
    resize_keyboard=True
)