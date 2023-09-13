from aiogram import Dispatcher
from .databese_middlewares import GetDBUser


def setup(dp: Dispatcher):
    dp.middleware.setup(GetDBUser())