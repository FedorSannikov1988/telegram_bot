import aiosqlite
from pathlib import Path


class Database_async:
    def __init__(self, db_path: str | Path = 'shop_database.db'):
        self.db_path = db_path

    async def execute(self, sql: str, parameters: tuple = tuple(),
                      fetchone=False, fetchall=False, commit=False):
        async with aiosqlite.connect(self.db_path) as connect_db:
            data = None
            cursor = await connect_db.cursor()
            await cursor.execute(sql, parameters)
            if commit:
                await connect_db.commit()
            if fetchone:
                data = await cursor.fetchone()
            if fetchall:
                data = await cursor.fetchall()
            return data

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY NOT NULL,
        phone VARCHAR(12)
        );
        """
        await self.execute(sql=sql, commit=True)

    async def create_table_products(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(300),
        quantity UNSIGNED INT,
        photo_path text
        );
        """
        await self.execute(sql, commit=True)

    async def add_user(self, id: int, phone: str = None):
        sql = 'INSERT INTO Users(id, phone) VALUES(?, ?)'
        parameters = (id, phone)
        await self.execute(sql, parameters, commit=True)

    async def add_product(self, name: str = None, quantity: int = 0, photo_path: str = ''):
        sql = 'INSERT INTO Products(name, quantity, photo_path) VALUES(?, ?, ?)'
        parameters = (name, quantity, photo_path)
        await self.execute(sql, parameters, commit=True)

    async def select_user_info(self, **kwargs):
        sql = 'SELECT * FROM Users WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, parameters, fetchall=True)

    async def select_product_info(self, **kwargs):
        sql = 'SELECT * FROM Products WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, parameters, fetchall=True)

    async def select_all_users(self):
        sql = 'SELECT * FROM Users'
        return await self.execute(sql, fetchall=True)

    async def select_all_products(self):
        sql = 'SELECT * FROM Products'
        return await self.execute(sql, fetchall=True)

    async def update_user_phone(self, id: int, phone: str):
        sql = 'UPDATE Users SET phone=? WHERE id=?'
        return await self.execute(sql, parameters=(phone, id), commit=True)

    async def update_product_quantity(self, id: int, quantity: int):
        sql = 'UPDATE Products SET quantity=? WHERE name=?'
        return await self.execute(sql, parameters=(quantity, id), commit=True)

    async def get_products_quantity(self) -> int:
        sql = 'SELECT * FROM Products'
        return len(await self.execute(sql, fetchall=True))

    async def delete_user(self, **kwargs):
        sql = 'DELETE FROM Users WHERE '
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, parameters=parameters, commit=True)

    async def delete_product(self, **kwargs):
        sql = 'DELETE FROM Products WHERE '
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, parameters=parameters, commit=True)

    async def delete_all_users(self):
        await self.execute('DELETE FROM Users WHERE True', commit=True)

    async def delete_all_products(self):
        await self.execute('DELETE FROM Products WHERE True', commit=True)

    async def drop_all_tables(self):
        await self.execute('DROP TABLE Users', commit=True)
        await self.execute('DROP TABLE Products', commit=True)

    @staticmethod
    def format_args(sql, parameters: dict) -> tuple:
        sql += ' AND '.join([
            f'{item} = ?' for item in parameters
        ])
        return sql, tuple(parameters.values())
