from aiogram import Dispatcher
from .databese_middlewares import GetTestInfo, GetProductInfo, GetUserCartInfo


def setup(dp: Dispatcher):
    dp.middleware.setup(GetTestInfo())