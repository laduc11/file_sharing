import socket
import os

IP = socket.gethostbyname(socket.gethostname())
IP_ADDR = "10.0.189.56"
PORT = 5500
ADDR = (IP_ADDR, PORT)
SIZE = 1024
ENCODING = "utf-8"


def main():
    client_welcome = ADDR
    print(client_welcome)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send(IP.encode(ENCODING))
    while True:
        command = input("> ")
        if (command == "CLOSE"):
            client.send(command.encode(ENCODING))
            os._exit(os.EX_OK)
        else:
            print("Syntax error")
        




if __name__ == "__main__":
    main()
