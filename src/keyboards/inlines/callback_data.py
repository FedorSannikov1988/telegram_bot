from aiogram.utils.callback_data import CallbackData

#возможно имело смысл сделать поизящнее navigation_cart_callback
navigation_cart_callback = \
    CallbackData('navigation_products_btm', 'cart', 'for_delete_cart', 'for_buy_cart')

navigation_items_callback = \
    CallbackData('navigation_products_btm', 'for_data', 'id', 'number_purchases')
