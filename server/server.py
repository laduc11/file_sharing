import socket
import os
import threading
from pythonping import ping
# import sys

import file_manage as fm

IP = socket.gethostbyname(socket.gethostname())
PORT = 16607
ADDR = (IP, PORT)
SIZE = 1024
ENCODING = "utf-8"
DATA_PATH = "data/"


# Create and set up database
def file_manage():
    db = fm.Sql()
    return db


def add_file(db, ip, client_name, filenames):
    duplicate = []
    filename_list = filenames.split(" ")
    for filename in filename_list:
        try:
            db.add(ip, client_name, filename)
        except fm.sql.IntegrityError:
            duplicate += [filename]
    return duplicate


def del_file(db, ip, filename):
    db.delete_file(ip, filename)


def print_list(list_file):
    result = ""
    for file in list_file:
        result += ' '.join(file) + '\n'
    return result


# Ping to client
# Return True if client is online
def ping(conn):
    try:
        conn.send("PING".encode(ENCODING))
        data = conn.recv(SIZE).decode(ENCODING)
    except Exception:
        print("Client is offline")
        return False

    if data == "ACCEPT":
        return True
    print("Client is not accept to connect")
    return False


# Catch command from client
def client_handle(conn, addr, db, client_name):
    print(f"New connection: {client_name}, {addr[0]}")
    is_close = False
    while True:
        data = conn.recv(SIZE).decode(ENCODING)
        data = data.split("$")
        
        if len(data) == 2:
            command, data = data
        else:
            command = data[0]

        if command == "CLOSE":
            # Close the server
            db.close_server()
            print(f"Server {ADDR} is closed")
            is_close = True
            conn.send(f"DISCONNECTED$Server {ADDR} is closed".encode(ENCODING))
            break

        elif command == "LOGOUT":
            # Disconnect to the server
            print(f"Client's IP {addr[0]} is disconnected")
            conn.send(f"DISCONNECTED${addr[0]} disconnected".encode(ENCODING))
            break

        elif command == "ADD":
            # Add new file into server table
            # Data: Name of file which need to be added
            # Client's IP = addr[0]
            # Filename = data
            duplicate = add_file(db, addr[0], client_name, data)
            print("add")
            if not duplicate:
                conn.send("OK$ADD FILE SUCCESSFULLY".encode(ENCODING))
            else:
                filenames = "Duplicate files: " + duplicate[0]
                for i in range(1, len(duplicate)):
                    filenames += ", " + duplicate[i]
                conn.send(f"OK$ {filenames}.".encode(ENCODING))

        elif command == "DELETE":
            # Delete file from server table
            # Data: Name of file which need to be deleted
            # Client's IP = addr[0]
            # File name = data
            del_file(db, addr[0], data)
            print("delete")
            conn.send("OK$DELETE FILE SUCCESSFULLY".encode(ENCODING))

        elif command == "LIST":
            # Send server table to client
            # Syntax "OK$<server table>"
            list_file = db.list()
            print(list_file)
            print("list")
            conn.send(f"OK${print_list(list_file)}".encode(ENCODING))
        elif command == "DOWNLOAD":
            # Syntax DOWNLOAD$<file_name>&<client's IP>
            # Download the file from client that have <IP>

            # Check client's status
            conn.send("PING".encode(ENCODING))
            wait = threading.Timer(2.0, lambda:print(conn.recv(SIZE).decode(ENCODING)))
            wait.start()

            # Inform download successfully
            print("download")
            conn.send("OK$Download successfully".encode(ENCODING))

        elif command == "LOCAL":
            # Command run on client
            # Server do nothing
            conn.send("LOCAL".encode(ENCODING))
            
        print(data)     # DEBUG
    
    conn.close()
    if is_close:
        os._exit(os.EX_OK)


def main():
    print("Server is online")
    db = file_manage()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"Server is listening in {IP}")
    while True:
        conn, addr = server.accept()

        # Get IP and name of client
        data = conn.recv(SIZE).decode(ENCODING)
        print(data)
        ip, client_name = data.split("$")
        addr = (ip, addr[1])
        conn.send(f"OK$Welcome {addr} to {ADDR}".encode(ENCODING))

        # Create threads for clients

        thread = threading.Thread(target=client_handle, args=(conn, addr, db, client_name))
        thread.start()


if __name__ == "__main__":
    main()
