# import socket
# import threading
# import os

from client_lib import *

# HOST_NAME = socket.gethostname()
# IP = socket.gethostbyname(HOST_NAME)
# IP_DST = "10.0.189.56"
# PORT = 16607
# MY_ADDR = (IP, PORT)
# ADDR = (IP_DST, PORT)
# SIZE = 1024
# ENCODING = "utf-8"
# DATA_PATH = "data/"




# Wait another client connect
def wait_connect(client):
    # client.bind(MY_ADDR)
    # client.listen()
    # print(f"Host {MY_ADDR} is listening")
    # conn, addr = client.accept()

    # data = conn.recv(SIZE).decode(ENCODING)     # Syntax: IP$host_name
    # data = data.split('$')
    # addr = (data[0], addr[1])

    # conn.send(f"Hello {addr} from {MY_ADDR}".encode(ENCODING))
    # while True:
    #     data = conn.recv(SIZE).decode(ENCODING)
    #     if data == "LOGOUT":
    #         conn.close()
    print("Multithread success")


# Client wait user type command
        
def main():
    # Create environment
    server_addr = ADDR
    print(server_addr)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send(f"{IP}${HOST_NAME}".encode(ENCODING))

    # Create socket to listen another client
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_thread = threading.Thread(target=host_mode, args=(host,))
    host_thread.start()

    while True:
        # Client receive request from server
        client_listen(client)

        # User send request to server
        # Write command
        command = input("> ")
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
        
        # Proccess user's command
        client_command(client, command, file_name)
    
    # os._exit(os.EX_OK)


if __name__ == "__main__":
    main()
