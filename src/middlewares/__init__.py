from aiogram import Dispatcher
from .databese_middlewares import GeTestInfo, GetProductInfo, GetUserCartInfo


def setup(dp: Dispatcher):
    dp.middleware.setup(GeTestInfo())