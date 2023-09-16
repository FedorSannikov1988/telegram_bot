from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from loader import db
import json


class GetUserCartInfo(BaseMiddleware):
    def __init__(self, dp):
        super().__init__()
        self.dp = dp

    async def on_process_message(self,
                                 message: types.Message,
                                 data: dict):

        text = message.text
        command = message.get_command()
        state_fsm = await self.dp.current_state().get_state()

        search_message_one: str = 'Корзина покупок'
        search_message_two: str = 'Shopping cart'
        search_command_one: str = '/cart'
        search_state_fsm_one: str = 'DeliveryState:wait_address'

        if (text is not None and search_message_one in text) or \
           (text is not None and search_message_two in text) or \
           (command is not None and search_command_one in command) or \
           (state_fsm is not None and search_state_fsm_one in state_fsm):

            user_id = message.from_user.id

            data = \
                await GetUserCartInfo.basket_formation(user_id=user_id,
                                                       data=data)

    async def on_process_callback_query(self,
                                        call: types.CallbackQuery,
                                        data: dict):

        to_check: str = call.data

        search_callback_one: str = \
            'navigation_products_btm:shopping cart:'
        search_callback_two: str = \
            'navigation_shopping_cart_btm:shopping cart:delete cart:'
        search_callback_three: str = \
            'navigation_shopping_cart_btm:shopping cart::buy cart'

        if (search_callback_one in to_check) or \
           (search_callback_two in to_check) or \
           (search_callback_three in to_check):

            user_id = call.from_user.id

            data = \
                await GetUserCartInfo.basket_formation(user_id=user_id,
                                                       data=data)

    @staticmethod
    async def basket_formation(user_id: int, data: dict) -> dict:

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
        return data


class GetProductInfo(BaseMiddleware):

    async def on_process_message(self,
                                 message: types.Message,
                                 data: dict):

        text = message.text
        command = message.get_command()

        search_message_one: str = 'Список товаров'
        search_message_two: str = 'List products'
        search_command_one: str = '/catalog'

        if (text is not None and search_message_one in text) or \
           (text is not None and search_message_two in text) or \
           (command is not None and search_command_one in command):

            first_product_info = await db.select_product_info(id=1)
            first_product_info = first_product_info[0]
            data['first_product_info'] = first_product_info
        else:
            data['first_product_info'] = None

    async def on_process_callback_query(self,
                                        call: types.CallbackQuery,
                                        data: dict):

        to_check: str = call.data

        search_callback_one: str = \
            'navigation_products_btm:products:'
        search_callback_two: str = \
            'navigation_products_btm:buy product:'

        if search_callback_one in to_check or\
           search_callback_two in to_check:

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

    async def on_process_callback_query(self,
                                        call: types.CallbackQuery,
                                        data: dict):

        to_check: str = call.data

        search_callback_one: str = \
            'navigation_shopping_cart_btm:shopping cart::buy cart'

        if search_callback_one in to_check:
            user_id = call.from_user.id
            data['for_user_verification'] = \
                await db.select_user_info(id=user_id)
        else:
            data['for_user_verification'] = None
