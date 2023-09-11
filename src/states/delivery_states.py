from aiogram.dispatcher.filters.state import StatesGroup, \
                                             State


class DeliveryState(StatesGroup):
    wait_data = State()
    wait_time = State()
    wait_name_recipient_parcel = State()
    wait_address = State()
    wait_confirmation_order = State()

