import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5500
ADDR = (IP, PORT)
SIZE = 1024
ENCODING = "utf-8"


def main():
    client_welcome = ADDR
    print(client_welcome)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


if __name__ == "__main__":
    main()
