from aiogram.dispatcher.filters.state import State, StatesGroup


class DeliveryState(StatesGroup):
    wait_data = State()
    wait_time = State()
    wait_name_recipient_parcel = State()
    wait_address = State()

