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
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_thread = threading.Thread(target=host_mode,args=(host,))
    client_thread = threading.Thread(target=client_mode,args=(client,))

    host_thread.start()
    client_thread.start()


if __name__ == "__main__":
    main()
