"""
Start app/bot
"""
from aiogram.utils import executor
from handlers import dp
import middlewares

if __name__ == '__main__':
    middlewares.setup(dp)
    executor.start_polling(dispatcher=dp)
