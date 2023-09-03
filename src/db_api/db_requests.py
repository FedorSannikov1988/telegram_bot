import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path: str | Path = 'shop_database.db'):
        self.db_path = db_path

    @property
    def connection(self):
        return sqlite3.connect(self.db_path)

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY NOT NULL,
        phone VARCHAR(12)
        );
        """
        self.execute(sql, commit=True)

    def create_table_products(self):
        sql = """ 
        CREATE TABLE IF NOT EXISTS Products(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name VARCHAR(300),
		quantity UNSIGNED INT
        );
        """
        self.execute(sql, commit=True)

    def add_user(self, id: int, phone: str = None):
        sql = 'INSERT INTO Users(id, phone) VALUES(?, ?)'
        parameters = (id, phone)
        self.execute(sql, parameters, commit=True)

    def add_product(self, name: str, quantity: int):
        sql = 'INSERT INTO Products(name, quantity) VALUES(?, ?)'
        parameters = (name, quantity)
        self.execute(sql, parameters, commit=True)

    def select_user_info(self, **kwargs) -> list:
        sql = 'SELECT * FROM Users WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def select_product_info(self, **kwargs) -> list:
        sql = 'SELECT * FROM Products WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def select_all_users(self) -> list:
        sql = 'SELECT * FROM Users'
        return self.execute(sql, fetchall=True)

    def select_all_products(self) -> list:
        sql = 'SELECT * FROM Products'
        return self.execute(sql, fetchall=True)

    def update_user_phone(self, id: int, phone: str):
        sql = 'UPDATE Users SET phone=? WHERE id=?'
        return self.execute(sql, parameters=(phone, id), commit=True)

    def update_quantity_product(self, name: str, quantity: int):
        sql = 'UPDATE Products SET quantity=? WHERE name=?'
        return self.execute(sql, parameters=(quantity, name), commit=True)

    def delete_user(self, **kwargs):
        sql = 'DELETE FROM Users WHERE '
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return self.execute(sql, parameters=parameters, commit=True)

    def delete_product(self, **kwargs):
        sql = 'DELETE FROM Products WHERE '
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return self.execute(sql, parameters=parameters, commit=True)

    def delete_all_users(self):
        self.execute('DELETE FROM Users WHERE True', commit=True)

    def delete_all_products(self):
        self.execute('DELETE FROM Products WHERE True', commit=True)

    def drop_all_tables(self):
        self.execute('DROP TABLE Users', commit=True)

    @staticmethod
    def format_args(sql, parameters: dict) -> tuple:
        sql += ' AND '.join([
            f'{item} = ?' for item in parameters
        ])
        return sql, tuple(parameters.values())
