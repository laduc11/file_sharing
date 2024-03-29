import socket
import threading
import os
import tqdm
# import time


HOST_NAME = socket.gethostname()
IP = socket.gethostbyname(HOST_NAME)
PORT = 16607
MY_ADDR = (IP, PORT)
SIZE = 1024*1024*2
ENCODING = "utf-8"
DATA_PATH = "data/"

# IP_DST = "10.0.189.56"
# ADDR = (IP_DST, PORT)

# Check the correctness of IP
def is_ip_valid(ip):
    nums = ip.split('.')
    if len(nums) != 4:
        return False
    try:
        for num in nums:
            if int(num) < 0 or int(num) > 255:
                return False
    except Exception:
        return False
    return True


# Client wait for request from server
def client_listen(client):
    try:
        client.settimeout(10)
        command = client.recv(SIZE).decode(ENCODING)
    except TimeoutError:
        return
    command = command.split('$')
    if command[0] == "OK":
        # Syntax: OK$<data need to print>
        print(command[1])
    elif command[0] == "DISCONNECTED":
        # Syntax: DISCONNECTED$<data need to print>
        # Print and kill the client process
        print(command[1])
        os._exit(os.EX_OK)
    elif command[0] == "CLOSE":
        print(command[1])
        os._exit(os.EX_OK)
    elif command[0] == "LOCAL":
        # Command was executed
        return
    elif command == "PING":
        # Reply ping to server
        client.send("ACCEPT".encode(ENCODING))


def client_command(client, command, file_name, is_admin):
    # is_continue = False
    try:
        # Finite state machine
        if command == "CLOSE":
            # Close server
            if not is_admin:
                print("You can not close the server")
                client.send("LOCAL".encode(ENCODING))
                return
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
                    return
                    # is_continue = True
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
            client.send("LOCAL".encode(ENCODING))

        elif command == "LIST":
            # List  all file in the server table
            print("doing LIST function")
            client.send(f"{command}".encode(ENCODING))

        elif command == "DIR":
            # List all file in client repository
            print('\n'.join(os.listdir(DATA_PATH)))
            client.send("LOCAL".encode(ENCODING))

        elif command == "DISCOVERY":
            ip = file_name
            client.send(f"{command}${ip}".encode(ENCODING))

        elif command == "PING":
            ip = file_name
            client.send(f"{command}${ip}".encode(ENCODING))

        elif command == "CLEAR":
            if not is_admin:
                print("You are not an admin")
                client.send("LOCAL".encode(ENCODING))
                return
            print("Clear database")
            client.send("CLEAR".encode(ENCODING))

        elif command == "HELP":
            # Print the guideline
            print("ADD$<file_name>: publish new file from repository to server")
            print("DELETE$<file_name>: delete file from server")
            print("LOGOUT: disconnect to server")
            print("CLOSE: disconnect and close the server")
            print("DOWNLOAD$<file_name>&<client's IP>: download file named file_name from another client")
            print("LIST: list all the file which the server can reach")
            print("DIR: list all file in my repository")
            print("PING$<IP_Address>: Ping a client to check if client online or not")
            print("DISCOVERY$<IP_Address>: list all file in local client repository")
            print("CLEAR: delete all data in table")
            client.send("LOCAL".encode(ENCODING))
        else:
            print("Syntax Error")
            client.send("LOCAL".encode(ENCODING))
    except WindowsError as er:
        if er.errno == 10054:
            print("An existing connection was forcibly closed by the remote host")
        elif er.errno == 10061:
            print("The server is inactive")
        
        os._exit(os.EX_OK)

    # return is_continue


# Download function for client
def client_download(client, file_name):
    ip = client.recv(SIZE).decode(ENCODING)
    if ip[:2] == "OK":
        print(ip[3:])
        return
    host_addr = (ip, PORT)
    temp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_client.settimeout(2)
    try:
        temp_client.connect(host_addr)
    except TimeoutError:
        print("Time out")
        os._exit(os.EX_OK)
        
    temp_client.send(f"CONNECTED${IP}".encode(ENCODING))
    
    command = temp_client.recv(SIZE).decode(ENCODING)
    command = command.split('$')[1]
    if command != "SUCCESS":
        temp_client.send("LOGOUT".encode(ENCODING))
    else:
        temp_client.send(f"DOWNLOAD${file_name}".encode(ENCODING))
    
    while True:
        command = temp_client.recv(SIZE).decode(ENCODING)
        command = command.split('$')
        if command[0] == "SIZE":
            file_size = int(command[1])
            temp_client.send(f"OK${file_name}".encode(ENCODING))
            break

    # Start download file
    done = False
    temp_client.settimeout(10)
    progress = tqdm.tqdm(unit="B", 
                         unit_scale=True, 
                         unit_divisor=1024, 
                         total=file_size, 
                         desc=f"{file_name.split('&')[0]}")
    download_file = open(DATA_PATH + file_name.split('&')[0], "a+b")
    while not done:
        recv = temp_client.recv(SIZE)
        progress.update(len(recv))
        download_file.write(recv)

        download_file.seek(-5, 1)
        if download_file.read() ==  b"<END>":
            done = True
            download_file.seek(-1, 1)
            for i in range (5):
                download_file.write(b'')
            pass
    
    download_file.close()
    
    temp_client.settimeout(2)
    temp_client.send("LOGOUT".encode(ENCODING))
    # client.send("OK$DOWNLOAD SUCCESSFULLY".encode(ENCODING))
    

# Process command from another client or server
def client_handle(client):
    while True:
        try:
            command = client.recv(SIZE).decode(ENCODING)
        except WindowsError as er:
            if er.errno == 10038:
                return
            else:
                print(f"Window error code {er.errno}")
        command = command.split('$')

        if command[0] == "DOWNLOAD":
            client.send(f"SIZE${str(os.path.getsize(DATA_PATH + command[1].split('&')[0]))}".encode(ENCODING))
            pass
        elif command[0] == "OK":
            file_name = command[1]
            file_data = open(DATA_PATH + file_name.split('&')[0], "rb").read() + b"<END>"
            client.sendall(file_data)
        elif command[0] == "LOGOUT":
            client.close()
            return
            
       


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
            # First message from another client
            # Syntax CONNECTED$<Client's IP>
            data = data.split('$')
            addr = (data[1], addr[1])
            conn.send("CONNECTED$SUCCESS".encode(ENCODING))
            # Debug
            print(f"{MY_ADDR} has connected to {addr}")

            client_handle(conn)

        new_client = threading.Thread(target=client_handle, args=(conn,))
        new_client.start()


# Run client mode
# Function: receive and send request to server, get and process command from user
def client_mode(client, server_ip, is_admin):
    # Create environment
    server_addr = (server_ip, PORT)
    print(server_addr)
    try:
        client.settimeout(2)
        client.connect(server_addr)
    except ConnectionRefusedError:
        print("Connection refused")
        os._exit(os.EX_OK)
    except TimeoutError:
        print("Time out")
        os._exit(os.EX_OK)
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
        client_command(client, command, file_name, is_admin)

    # os._exit(os.EX_OK)
