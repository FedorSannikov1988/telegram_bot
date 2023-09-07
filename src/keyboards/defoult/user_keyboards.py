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
                KeyboardButton(text='Список товаров'),
                KeyboardButton(text='Корзина покупок'),
                KeyboardButton(text='Регистрация',
                               request_contact=True),
            ],
            [
                KeyboardButton(text='Разработчик'),
                KeyboardButton(text='Скрыть меню')
            ]
        ],
        resize_keyboard=True
)