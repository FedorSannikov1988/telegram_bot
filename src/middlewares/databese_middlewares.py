from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from loader import db


class GetDBUser(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        data['user_basket'] = f'{message.from_user.id}'
        # await db.select_user_cart(id = message.from_user.id)

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        pass