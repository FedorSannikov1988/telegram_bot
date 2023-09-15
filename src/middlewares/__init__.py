from aiogram import Dispatcher
from .databese_middlewares import GetUserCartInfo, \
                                  GetProductInfo, \
                                  GetTestInfo, \
                                  GetUserInfo


def setup(dp: Dispatcher):
    dp.middleware.setup(GetTestInfo())