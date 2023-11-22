import socket
import os

HOST_NAME = socket.gethostname()
IP = socket.gethostbyname(HOST_NAME)
<<<<<<< HEAD
IP_DST = "10.0.189.56"
PORT = 16607
=======
IP_DST = "10.230.20.207"
PORT = 160607
>>>>>>> 84ae46e5fb3ca1fc7fe7b8fbef554e15ba23b683
ADDR = (IP_DST, PORT)
SIZE = 1024
ENCODING = "utf-8"
DATA_PATH = "data/"


def main():
    server_addr = ADDR
    print(server_addr)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send(f"{IP}${HOST_NAME}".encode(ENCODING))
    while True:
        # Client recieve request from server
        command = client.recv(SIZE).decode(ENCODING)
        command = command.split("$")
        if command[0] == "OK":
            print(command[1])
        elif command[0] == "DISCONNECTED":
            print(command[1])
            break

        # User send request to server
        # Write command
        command = input("> ")
        command = command.split("$")

        # Check and analize command
        if len(command) == 1:
            command = ''.join(command)
        elif len(command) == 2:
            command, file_name = command
        else:
            print("Syntax Error")
            continue
        
        # Finite machine state
        if command == "CLOSE":
            # Close server
            print("Server is closing")
            client.send(command.encode(ENCODING))
            break
        elif command == "LOGOUT":
            # Disconnect from server
            print(f"{IP} is disconnecting")
            client.send(f"{command}".encode(ENCODING))
        elif command == "ADD":
            # Public file in server
            if file_name == ".":
                data = ' '.join(os.listdir(DATA_PATH))
            else:
                flag = False
                for file in os.listdir(DATA_PATH):
                    if file == file_name:
                        flag = True
                        break
                
                if not flag:
                    print("File is invalid")
                    continue
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
        elif command == "HELP":
            # Print the guildline
            print("ADD$<file_name>: add new file from repository to server")
            print("DELETE$<file_name>: delete file from server")
            print("LOGOUT: disconnect to server")
            print("CLOSE: disconnect and close the server")
            print("DOWNLOAD$<file_name>&<client's IP>")
            print("LIST: list all the file which the server can reach")
        else:
            print("Syntax Error")
    
    os._exit(os.EX_OK)

        




if __name__ == "__main__":
    main()
