import sqlite3 as sql

db = sql.connect("test.db")
cursor = db.cursor()
cursor.execute("drop table New_table")
cursor.execute(f"""CREATE TABLE New_table(
                IP_Address char(15),
                Client_name varchar(30),
                File_name varchar(30),
                primary key(IP_Address, File_name))""")


def add(ip, client, file):
    cursor.execute(f"""insert into New_table(IP_Address, Client_name, File_name)VALUES('{ip}', '{client}', '{file}') """)
    db.commit()


add("192.168.0.1", "Hai", "test.txt")
add("192.168.0.2", "name", "text.txt")

cursor.execute("select * from New_table")
customers = cursor.fetchall()

for customer in customers:
    print(type(customer))

db.close()