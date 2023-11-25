import socket
import threading
import os
import tqdm
import time


HOST_NAME = socket.gethostname()
IP = socket.gethostbyname(HOST_NAME)
IP_DST = "192.168.137.11"
PORT = 16607
MY_ADDR = (IP, PORT)
ADDR = (IP_DST, PORT)
SIZE = 1024
ENCODING = "utf-8"
DATA_PATH = "data/"


# Client wait for request from server
def client_listen(client):
    command = client.recv(SIZE).decode(ENCODING)
    command = command.split('$')
    if command[0] == "OK":
        # Syntax: OK$<data need to print>
        print(command[1])
    elif command[0] == "DISCONNECTED":
        # Syntax: DISCONNECTED$<data need to print>
        # Print and kill the client process
        print(command[1])
        exit()
    elif command[0] == "CLOSE":
        print(command[1])
        os._exit(os.EX_OK)
    elif command[0] == "LOCAL":
        # Command was executed
        pass
    elif command == "PING":
        # Reply ping to server
        client.send("ACCEPT".encode(ENCODING))


def client_command(client, command, file_name):
    is_continue = False
    try:
        # Finite state machine
        if command == "CLOSE":
            # Close server
            print("Server is closing")
            client.send(command.encode(ENCODING))

        elif command == "LOGOUT":
            # Disconnect from server
            print(f"{IP} is disconnecting")
            client.send(f"{command}".encode(ENCODING))

        elif command == "ADD":
            # Public file in server
            if file_name == ".":
                # Public all the file in client repository to server 
                data = ' '.join(os.listdir(DATA_PATH))
            else:
                # Check file name
                flag = False
                for file in os.listdir(DATA_PATH):
                    if file == file_name:
                        flag = True
                        break

                if not flag:
                    print("File is invalid")
                    client.send("LOCAL".encode(ENCODING))
                    is_continue = True
                else:
                    data = file_name

            client.send(f"{command}${data}".encode(ENCODING))
        elif command == "DELETE":
            # Send request delete file to server
            client.send(f"{command}${file_name}".encode(ENCODING))

        elif command == "DOWNLOAD":
            # Fetch the copy file from another client repository
            client.send(f"{command}${file_name}".encode(ENCODING))
            client_download(client, file_name)
        elif command == "LIST":
            # List  all file in the server table
            print("doing LIST function")
            client.send(f"{command}".encode(ENCODING))

        elif command == "DIR":
            # List all file in client repository
            print('\n'.join(os.listdir(DATA_PATH)))
            client.send("LOCAL".encode(ENCODING))

        elif command == "HELP":
            # Print the guideline
            print("ADD$<file_name>: publish new file from repository to server")
            print("DELETE$<file_name>: delete file from server")
            print("LOGOUT: disconnect to server")
            print("CLOSE: disconnect and close the server")
            print("DOWNLOAD$<file_name>&<client's IP>")
            print("LIST: list all the file which the server can reach")
            print("DIR: list all file in my repository")
            client.send("LOCAL".encode(ENCODING))
        else:
            print("Syntax Error")
            client.send("LOCAL".encode(ENCODING))
    except ConnectionResetError:
        print("Server is closed")
        exit()

    return is_continue


# Download function for client
def client_download(client, file_name):
    ip = client.recv(SIZE).decode(ENCODING)
    host_addr = (ip, PORT)
    temp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_client.connect(host_addr)
    thread = threading.Timer(0.05, lambda:temp_client.send(f"CONNECTED${IP}".encode(ENCODING)))
    thread.start()
    command = temp_client.recv(SIZE).decode(ENCODING)
    command = command.split('$')[1]
    if command != "SUCCESS":
        temp_client.send("LOGOUT".encode(ENCODING))
    else:
        temp_client.send(f"DOWNLOAD${file_name}")
    
    while True:
        command = temp_client.recv(SIZE).decode(ENCODING)
        command = command.split('$')
        if command[0] == "SIZE":
            file_size = int(command[1])
            temp_client.send(f"OK${file_name}".encode(ENCODING))
            break

    # Start download file
    done = False
    data = b""
    progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=file_size)
    while not done:
        data += temp_client.recv(SIZE)
        progress.update(SIZE)
        if data[-5:] == "<END>":
            done = True
            data = data[:-5]

    with open(DATA_PATH + file_name, "wb") as download_file:
        download_file.write(data)
    
    temp_client.send("LOGOUT".encode(ENCODING))
    print("DOWNLOAD SUCCESSFULLY")
    


# Process command from another client or server
def client_handle(client):
    while True:
        command = client.recv(SIZE).decode(ENCODING)
        command = command.split('$')

        if command[0] == "DOWNLOAD":
            client.send(f"SIZE${str(os.path.getsize(DATA_PATH + file_name))}".encode(ENCODING))
            pass
        elif command[0] == "OK":
            file_name = command[1]
            file_data = open(DATA_PATH + file_name, "rb").read()
            client.sendall(file_data)
        elif command[0] == "LOGOUT":
            client.send("DISCONNECTED".encode(ENCODING))
            break
    
    client.close()     


# Run host mode
# Function: Ping, receive file from another client
def host_mode(host):
    host.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host.bind(MY_ADDR)
    host.listen()
    print(f"Client {MY_ADDR} is listening")
    
    while True:
        conn, addr = host.accept()
        # if server then data = "PING"
        # if client then data = "Client's IP$host_name"
        data = conn.recv(SIZE).decode(ENCODING)
        
        if data == "PING":
            # Send confirm message to server
            conn.send("ACCEPT".encode(ENCODING))
            continue
        else:
            # First mesage from another client
            # Syntax CONNECTED$<Client's IP>
            data = data.split('$')
            addr = (data[1], addr[1])
            conn.send("CONNECTED$SUCCESS".encode(ENCODING))
            # Debug
            print(f"{MY_ADDR} has connected to {addr}")

        new_client = threading.Thread(target=client_handle, args=(conn,))
        new_client.start()


# Run client mode
# Function: receive and send request to server, get and process command from user
def client_mode(client):
    # Create environment
    server_addr = ADDR
    print(server_addr)
    client.connect(ADDR)
    client.send(f"{IP}${HOST_NAME}".encode(ENCODING))

    while True:
        # Client receive request from server
        client_listen(client)

        # User send request to server
        # Write command
        command = input(">>> ")
        command = command.split("$")

        # Check and analyze command
        file_name = ""
        if len(command) == 1:
            command = ''.join(command)
        elif len(command) == 2:
            command, file_name = command
        else:
            print("Syntax Error")
            continue

        # Process user's command
        client_command(client, command, file_name)

    # os._exit(os.EX_OK)

    pass
