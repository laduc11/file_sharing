from server_lib import *


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    create_server(server)


if __name__ == "__main__":
    main()
