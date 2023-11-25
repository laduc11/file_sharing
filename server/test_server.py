import file_manage


db = file_manage.Sql().find('10.230.20.207', 'meo.txt')
# find = db.find('10.230.20.207', 'meo.txt')
print(db)
