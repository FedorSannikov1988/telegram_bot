"""
Class for FSM State
"""
from aiogram.dispatcher.filters.state import StatesGroup, \
                                             State


class DeliveryState(StatesGroup):
    """
    Conditions for making delivery.
    """
    wait_data = State()
    wait_time = State()
    wait_name_recipient_parcel = State()
    wait_address = State()
    wait_confirmation_order = State()


class QuestionnaireState(StatesGroup):
    """
    Conditions for conducting a survey of the buyer.
    """
    wait_what_like = State()
    wait_announcement_results = State()


class MoneyState(StatesGroup):
    """
    Conditions for depositing money to a personal account.
    """
    wait_amounts_money = State()


