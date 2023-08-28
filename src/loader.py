from aiogram import Dispatcher, \
                    Bot
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)