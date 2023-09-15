from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from loader import db
import json


class GetTestInfo(BaseMiddleware):

    async def on_process_message(self, message: types.Message, data: dict):
        data['test_middlewares'] = f'{message.from_user.id}'

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        data['test_middlewares'] = f'{call.from_user.id}'


class GetUserCartInfo(BaseMiddleware):

    async def on_process_message(self,
                                 message: types.Message,
                                 data: dict):

        user_id = message.from_user.id
        cart_user = await db.select_user_cart(user_id=user_id)

        if cart_user:
            cart_user_dict = json.loads(cart_user[0][2])

            for id_product, quantity_product in cart_user_dict.items():
                name_product = await db.select_product_info(id=id_product)
                if 'cart_user_info' not in data.keys():
                    data['cart_user_info'] = {name_product[0][1]: quantity_product}
                else:
                    data['cart_user_info'].update({name_product[0][1]: quantity_product})
        else:
            data['cart_user_info'] = None

    async def on_process_callback_query(self,
                                        call: types.CallbackQuery,
                                        data: dict):

        user_id = call.from_user.id
        cart_user = await db.select_user_cart(user_id=user_id)

        if cart_user:
            cart_user_dict = json.loads(cart_user[0][2])

            for id_product, quantity_product in cart_user_dict.items():
                name_product = await db.select_product_info(id=id_product)
                if 'cart_user_info' not in data.keys():
                    data['cart_user_info'] = {name_product[0][1]: quantity_product}
                else:
                    data['cart_user_info'].update({name_product[0][1]: quantity_product})
        else:
            data['cart_user_info'] = None


class GetProductInfo(BaseMiddleware):

    async def on_process_message(self,
                                 message: types.Message,
                                 data: dict):

        first_product_info = await db.select_product_info(id=1)
        first_product_info = first_product_info[0]
        data['first_product_info'] = first_product_info

    async def on_process_callback_query(self,
                                        call: types.CallbackQuery,
                                        data: dict):

        to_check: str = call.data

        if 'navigation_products_btm:products:' in to_check \
                or 'navigation_products_btm:buy product:' in to_check:

            current_product_id = int(call.data.split(':')[-2])
            data['product_info'] = \
                await db.select_product_info(id=current_product_id)
        else:
            data['product_info'] = None


class GetUserInfo(BaseMiddleware):

    async def on_process_message(self,
                                 message: types.Message,
                                 data: dict):

        if message.contact:

            user_id: int = int(message.contact.user_id)
            user_phone: str = str(message.contact.phone_number)
            search_results_user = \
                await db.select_user_info(id=user_id,
                                          phone=user_phone)

            data['contact_user_id'] = user_id
            data['contact_user_phone'] = user_phone
            data['search_results_user'] = search_results_user

        else:

            data['contact_user_id'] = None
            data['contact_user_phone'] = None
            data['search_results_user'] = None
