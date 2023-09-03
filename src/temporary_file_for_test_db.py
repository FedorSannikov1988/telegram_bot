import asyncio
from loader import db

#для тестирования бд
#я удалю файл когда
#определюсь окончательно с БД

# sql = """
# CREATE TABLE IF NOT EXISTS Users(
# id INTEGER PRIMARY KEY NOT NULL,
# phone VARCHAR(12)
# );
# """
#asyncio.run(db.execute(sql=sql, commit=True))
#asyncio.run(db.create_table_users())
#asyncio.run(db.create_table_products())
#asyncio.run(db.add_user(id=660024517, phone=777))
#asyncio.run(db.add_product(name='test', quantity=1))
#print(asyncio.run(db.select_user_info(id=660024517)))
#print(asyncio.run(db.select_product_info(name='test')))
asyncio.run(db.update_user_phone(id='660024517', phone='888' ))
asyncio.run(db.update_quantity_product(name='test', quantity='8'))
print(asyncio.run(db.select_all_users()))
print(asyncio.run(db.select_all_products()))

#db.add_user(id=660024517, phone=777)
#print(db.select_all_users())
#print(db.select_user_info(id=660024516))
#print(db.delete_user(id=660024516))
#db.add_product(name='test', quantity=1)
#print(db.select_all_products())
#print(db.select_product_info(id=1, name='test'))
#print(db.delete_product(id=1))
#print(db.select_all_products())
