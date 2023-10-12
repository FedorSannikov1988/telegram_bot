"""
To pay for a purchase
"""
from .validation_amounts_money import ValidationAmountsMoney
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold
from answers import all_answer_for_user
from aiogram.types import ContentType
from loader import db, dp, bot
from states import MoneyState
from config import TOKEN_UPAY
from aiogram import types


@dp.message_handler(commands=['money'])
async def add_money(message: types.Message, search_results_user: list):
    """
    Launching a chain of handlers to replenish the wallet.

    :param message: types.Message
    :param search_results_user: list
    :return: None
    """
    if search_results_user:
        text: str = all_answer_for_user['give_money_p1']['ru']
        await MoneyState.wait_amounts_money.set()
    else:
        text: str = all_answer_for_user['give_money_p2']['ru']
    await message.answer(text=text)


@dp.message_handler(state=MoneyState.wait_amounts_money)
async def enter_amounts_money(message: types.Message, state: FSMContext):
    """
    Entering the amount for which the user wants to replenish
    the personal wallet (with subsequent validation of the entered amount).

    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    money: str = message.text

    if ValidationAmountsMoney().validation_amount(multiplicity=50,
                                                  money=money,
                                                  min=100):
        money_for_amount: int = int(money) * 100
        await state.reset_state()

        await bot.send_invoice(chat_id=message.from_user.id,
                               title="Пополнение баланса",
                               description=f"Пополнение баланса "
                                           f"на {money} Рублей",
                               payload='add_money',
                               provider_token=TOKEN_UPAY,
                               currency="RUB",
                               start_parameter="add_money",
                               prices=[{
                                   "label": "Rub",
                                   "amount": money_for_amount
                               }])
    else:
        text: str = all_answer_for_user['give_money_p1']['ru']
        await message.answer(text=text)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    """
    Displaying a message about adding an item to the cart
    :param pre_checkout_query: types.PreCheckoutQuery
    :return: None
    """
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message, wallet_info: list):
    """
    Adding money to the user's personal wallet if the money
    transaction to the store account is completed successfully.

    :param message: types.Message
    :param wallet_info: list
    :return: None
    """
    if message.successful_payment.invoice_payload == "add_money":

        user_id: int = int(message.from_user.id)
        cash = message.successful_payment.total_amount
        cash = cash / 100

        if not wallet_info:
            await db.add_wallet_user(user_id=user_id, cash=cash)
        else:
            wallet_info = wallet_info[0]
            cash += wallet_info[2]
            await db.update_user_wallet(user_id=user_id, cash=cash)
        text: str = f"{all_answer_for_user['give_money_p3_v1']['ru']}" \
                    f"{cash} {all_answer_for_user['give_money_p3_v2']['ru']}"
    else:
        text: str = all_answer_for_user['give_money_p4']['ru']

    await message.answer(text=hbold(text))