from aiogram import Dispatcher
from .databese_middlewares import GetUserCartInfo, \
                                  GetProductInfo, \
                                  GetWalletInfo, \
                                  GetUserInfo


def setup(dp: Dispatcher):
    dp.middleware.setup(GetUserCartInfo(dp=dp))
    dp.middleware.setup(GetProductInfo())
    dp.middleware.setup(GetWalletInfo())
    dp.middleware.setup(GetUserInfo())
