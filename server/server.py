import socket
import os
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 5500
ADDR = (IP, PORT)
SIZE = 1024
ENCODING = "utf-8"

def main():
    print("Server is online")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("Server is listening")
    while True:
        connect, addr = server.accept()
        print(f"New connection: {addr}")

if __name__ == "__main__":
    main()