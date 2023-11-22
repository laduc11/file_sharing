import socket
import os
import threading
import sys

import file_manage as fm

IP = socket.gethostbyname(socket.gethostname())
PORT = 5500
ADDR = (IP, PORT)
SIZE = 1024
ENCODING = "utf-8"
DATA_PATH = "data/"

# Catch command from client
def client_handle(conn, addr):
    print(f"New connection: {addr[0]}")
    while True:
        data = conn.recv(SIZE).decode(ENCODING)
        if data == "CLOSE":
            # Close the server
            print(f"{addr[0]} disconnected")
            os._exit(os.EX_OK)
        
    



def main():
    print("Server is online")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"Server is listening in {IP}")
    while True:
        conn, addr = server.accept()

        # Get IP of client
        data = conn.recv(SIZE).decode(ENCODING)
        addr = (data ,addr[1])

        # Create threads for clients
        thread = threading.Thread(target=client_handle, args=(conn, addr))
        thread.start()



if __name__ == "__main__":
    main()
