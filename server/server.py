import socket
import os
import threading
import sys

IP = socket.gethostbyname(socket.gethostname())
PORT = 5500
ADDR = (IP, PORT)
SIZE = 1024
ENCODING = "utf-8"
DATA_PATH = "data/"

# Catch command from client
def client_handle(conn, addr):
    print(f"New connection: {addr[0]}")
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
            print(f"server {ADDR} is closed")
            is_close = True
            break
        elif command == "LOGOUT":
            # Disconnect to the server
            conn.send(f"{addr[0]} disconnected".encode(ENCODING))
            break
        elif command == "ADD":
            # Add new file into server table
            # Data: Name of file which need to be added
            # Client's IP = addr[0]
            print("add")
            conn.send("OK$ADD FILE SUCCESSFULLY".encode(ENCODING))
        elif command == "DELETE":
            # Delete file from server table
            # Data: Name of file which need to be deleted
            # Client's IP = addr[0]
            print("delete")
            conn.send("OK$DELETE FILE SUCCESSFULLY".encode(ENCODING))
        elif command == "LIST":
            # Send server table to client
            # Syntax "OK$<server table>"
            print("list")
            conn.send("OK$LIST SUCCESSFULLY".encode(ENCODING))

        print(data)     # DEBUG
    
    conn.close()
    if is_close:
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
        conn.send(f"OK$Welcome to {ADDR}".encode(ENCODING))

        # Create threads for clients
        thread = threading.Thread(target=client_handle, args=(conn, addr))
        thread.start()



if __name__ == "__main__":
    main()