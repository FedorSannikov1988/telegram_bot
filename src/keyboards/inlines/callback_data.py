from aiogram.utils.callback_data import CallbackData


navigation_items_callback = \
    CallbackData('navigation_products_btm',
                 'for_data', 'id', 'number_purchases')

navigation_cart_callback = \
    CallbackData('navigation_shopping_cart_btm',
                 'operations_inside_bucket', 'for_delete_cart', 'for_buy_cart')
