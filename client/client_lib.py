import socket
import threading
import os


HOST_NAME = socket.gethostname()
IP = socket.gethostbyname(HOST_NAME)
IP_DST = "10.0.189.56"
PORT = 16607
MY_ADDR = (IP, PORT)
ADDR = (IP_DST, PORT)
SIZE = 1024
ENCODING = "utf-8"
DATA_PATH = "data/"


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
    elif command[0] == "LOCAL":
        # Command was excuted
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
        elif command == "LIST":
            # List  all file in the server table
            print("doing LIST function")
            client.send(f"{command}".encode(ENCODING))

        elif command == "DIR":
            # List all file in client repository
            print('\n'.join(os.listdir(DATA_PATH)))
            client.send("LOCAL".encode(ENCODING))

        elif command == "HELP":
            # Print the guildline
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
