from aiogram.types import ReplyKeyboardMarkup, \
                          KeyboardButton

commands_start_keyboard = \
    ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Помощь'),
                KeyboardButton(text='Инструкция')
            ],
            [
                KeyboardButton(text='Меню'),
                KeyboardButton(text='Разработчик')
            ],
            [
                KeyboardButton(text='Зарегистрироваться',
                               request_contact=True),
                KeyboardButton(text='Скрыть меню')
            ]
        ],
        resize_keyboard=True
)