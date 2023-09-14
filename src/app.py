from aiogram.utils import executor
from middlewares import GetUserCartInfo, \
                        GetProductInfo, \
                        GeTestInfo
from handlers import dp
import middlewares

if __name__ == '__main__':
    #middlewares.setup(dp)
    dp.middleware.setup(GeTestInfo())
    dp.middleware.setup(GetProductInfo())
    dp.middleware.setup(GetUserCartInfo())
    executor.start_polling(dispatcher=dp)
