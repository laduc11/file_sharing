import socket
import os
import threading
# import time

import file_manage as fm

IP = socket.gethostbyname(socket.gethostname())
PORT = 16607
ADDR = (IP, PORT)
SIZE = 1024
ENCODING = "utf-8"
DATA_PATH = "data/"

db = fm.Sql()


# 10 Types of command receive
# Return message after processing the command
# CLOSE
def close_cmd():
    """Close the server"""
    db.close_server()
    print(f"Server {ADDR} is closed")
    return f"CLOSE$Server {ADDR} is closed"


# LOGOUT
def logout_cmd(addr):
    """Disconnect to server"""
    print(f"Client's IP {addr[0]} is disconnected")
    return f"DISCONNECTED${addr[0]} disconnected"


# LOCAL
def local_cmd():
    """Command run on client"""
    return "LOCAL"


# ADD
def add_file(ip, client_name, filenames):
    duplicate = []
    filename_list = filenames.split(" ")
    for filename in filename_list:
        try:
            db.add(ip, client_name, filename)
        except fm.sql.IntegrityError:
            duplicate += [filename]
    return duplicate


def add_cmd(addr, client_name, data):
    """Add client's public file into database"""
    duplicate = add_file(addr[0], client_name, data)
    print("add")
    if not duplicate:
        return "OK$ADD FILE SUCCESSFULLY"
    else:
        filenames = "Duplicate files: " + duplicate[0]
        for i in range(1, len(duplicate)):
            filenames += ", " + duplicate[i]
        return f"OK$ {filenames}."


# DELETE
def delete_cmd(ip, filename):
    """Remove client's file from server database"""
    db.delete_file(ip, filename)
    print("delete")
    return "OK$DELETE FILE SUCCESSFULLY"


# LIST
def print_list(list_file):
    res = ""
    for file in list_file:
        res += ' '.join(file) + '\n'
    res = list(res)
    del res[-1]
    res = ''.join(res)
    return res


def list_cmd():
    """Print the of list clients' file which can download through server's database"""
    list_file = db.list()
    list_file = print_list(list_file)
    print(list_file)
    print("list")
    return f"OK${list_file}"


# DOWNLOAD
def download_cmd(data):
    # Check file existence
    try:
        file_name, ip = data.split('&')
    except ValueError:
        return "OK$Syntax Error"
    if not db.find(ip, file_name):
        return "OK$File is not exist"
    
    # Live check client have file
    ping = ping_cmd(ip)[3:]
    ping = ping.split(' ')[-1]
    if ping == "online":
        msg = f"{ip}"
    else:
        msg = f"OK$Can not download file"
    return msg
    

# DISCOVERY
def discovery_cmd(ip):
    list_file = db.find_by_ip(ip)
    data = ""
    for file in list_file:
        data += ' '.join(file) + '\n'
    data = data[:-1]
    return f"OK${data}"

# PING
def ping_cmd(ip):
    try:
        socket.setdefaulttimeout(2)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((ip, PORT))
    except TimeoutError:
        return f"OK${ip} is offline"

    server.send("PING".encode(ENCODING))
    if server.recv(SIZE).decode(ENCODING) == "ACCEPT":
        msg = f"OK${ip} is online"
    else:
        msg = f"OK${ip} refuse to connect"

    return msg


# Process command and return reply message client
def process_command(data, addr, client_name):
    data = data.split("$")
    if len(data) == 2:
        command, data = data
    else:
        command = data[0]

    if command == "CLOSE":
        return close_cmd()

    elif command == "LOGOUT":
        return logout_cmd(addr)

    elif command == "LOCAL":
        return local_cmd()

    elif command == "ADD":
        # Add new file into server table
        # Data: Name of file which need to be added
        # Client's IP = addr[0]
        # Filename = data
        return add_cmd(addr, client_name, data)

    elif command == "DELETE":
        # Delete file from server table
        # Data: Name of file which need to be deleted
        # Client's IP = addr[0]
        # File name = data
        return delete_cmd(addr[0], data)

    elif command == "LIST":
        # Send server table to client
        # Syntax "OK$<server table>"
        return list_cmd()

    elif command == "PING":
        return ping_cmd(data)

    elif command == "DISCOVERY":
        return discovery_cmd(data)

    elif command == "DOWNLOAD":
        return download_cmd(data)


# Receive request from client and reply
def client_handle(conn, addr, client_name):
    print(f"New connection: {client_name}, {addr[0]}")
    while True:
        data = conn.recv(SIZE).decode(ENCODING)
        conn.send(process_command(data, addr, client_name).encode(ENCODING))
        # print(process_command(data, addr, client_name))
        # try:
        #     conn.send(process_command(data, addr, client_name).encode(ENCODING))
        # except Exception:
        #     print(conn.send(process_command(data, addr, client_name).encode(ENCODING)))
        #     os._exit(os.EX_OK)

        if data[:5] == "CLOSE" or data[:12] == "DISCONNECTED":
            break


    conn.close()
    if data[0:5] == "CLOSE":
        os._exit(os.EX_OK)


# Create server
def create_server(server):
    print("Server is online")
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
        thread = threading.Thread(target=client_handle, args=(conn, addr, client_name))
        thread.start()
