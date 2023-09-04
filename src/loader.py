from aiogram import Dispatcher, \
                    Bot
from db_api import Database_async
from db_api import Database
from config import TOKEN
from pathlib import Path
import aiosqlite
import asyncio
import sqlite3


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db_path = \
    Path('db_api', 'database', 'shop_database.db')
db = Database_async(db_path=db_path)
#db = Database(db_path=db_path)


async def create_all_preciso_table():
    task2 = asyncio.create_task(db.create_table_users())
    task3 = asyncio.create_task(db.create_table_products())
    await asyncio.gather(task2, task3)


try:

    # так работает (разбираюсь почему):
    # это не асинхронный запуск:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.create_table_users())
    loop.run_until_complete(db.create_table_products())
    #так не работает
    # asyncio.run(create_all_preciso_table())
    # и так не работает
    # asyncio.run(db.create_table_users())
    # asyncio.run(db.create_table_products())
    # db.create_table_users()
    # db.create_table_products()
except aiosqlite.OperationalError as sql_error:
    print(f'{sql_error = }')
#except sqlite3.OperationalError as sql_error:
#    print(f'{sql_error = }')
except Exception as all_error:
    print(f'{all_error = }')
