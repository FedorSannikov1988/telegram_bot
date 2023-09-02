from aiogram import Dispatcher, \
                    Bot
from db_api import Database
from config import TOKEN
from pathlib import Path
import sqlite3

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db_path = \
    Path('db_api', 'database', 'shop_database.db')
db = Database(db_path=db_path)

try:
    db.create_table_users()
except sqlite3.OperationalError as error:
    print(error)
except Exception as error:
    print(error)