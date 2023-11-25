import sqlite3 as sql


class Sql:
    def __init__(self):
        self.db = sql.connect("client_files.db", check_same_thread=False)
        self.table_name = "File_manage"
        self.cursor = self.db.cursor()
        self.create_table()

    def create_table(self):
        # self.drop_table()
        try:
            self.cursor.execute(
                f"""CREATE TABLE {self.table_name}(
                    IP_Address char(15),
                    Client_name varchar(30),
                    File_name varchar(30),
                    primary key(IP_Address, File_name))"""
            )
        except sql.OperationalError:
            print("File manage is ready to use")

    def drop_table(self):
        self.cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        self.db.commit()

    def add(self, ip, client, file):
        self.cursor.execute(
            f"INSERT INTO {self.table_name}(IP_Address, Client_name, File_name) VALUES('{ip}', '{client}', '{file}')"
        )
        self.db.commit()

    def delete_file(self, ip, file):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE IP_Address = '{ip}' AND File_name = '{file}'")
        self.db.commit()

    # def client_out(self, ip):
    #     self.cursor.execute(f"DELETE FROM {self.table_name} WHERE IP_Address = '{ip}'")
    #     self.db.commit()

    def list(self):
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = self.cursor.fetchall()
        return rows

    def close_server(self):
        self.db.close()

    def find(self, ip, file_name):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE IP_Address = '{ip}' AND File_name = '{file_name}'")
        rows = self.cursor.fetchall()
        return bool(len(rows))

