from loader import db

print(db.select_all_users())
print(db.select_user_info(id=660024516))
print(db.update_user_phone(id=660024516, phone='test'))
print(db.select_user_info(id=660024516))
print(db.delete_user(id=660024516))
print(db.select_all_users())