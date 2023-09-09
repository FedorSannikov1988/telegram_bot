from aiogram import Dispatcher, Bot
from db_api import Database_async
from config import TOKEN
from pathlib import Path
import aiosqlite
import asyncio


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db_path = \
    Path('db_api', 'database', 'shop_database.db')
db = Database_async(db_path=db_path)

try:
    loop = asyncio.get_event_loop()
    create_needs_tables = \
        [db.create_table_users(),
         db.create_table_products(),
         db.create_table_shopping_cart()]
    loop.run_until_complete(asyncio.gather(*create_needs_tables))
except aiosqlite.OperationalError as sql_error:
    # сдесь нужно написать и вставить логер
    print(f'{sql_error = }')
except Exception as all_error:
    # сдесь нужно написать и вставить логер
    print(f'{all_error = }')
