import file_manage
#
#
# db = file_manage.Sql().find('10.230.20.207', 'meo.txt')
# # find = db.find('10.230.20.207', 'meo.txt')
# print(db)

# a = "abcacacas"
#
# print(a[0:5])

db = file_manage.Sql()

list_address = db.select_address()
for address in list_address:
    print(type(address[0]))
