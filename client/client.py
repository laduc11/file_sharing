import socket
import os

IP = socket.gethostbyname(socket.gethostname())
IP_DST = "10.230.20.207"
PORT = 5500
ADDR = (IP_DST, PORT)
SIZE = 1024
ENCODING = "utf-8"
DATA_PATH = "data/"


def main():
    client_welcome = ADDR
    print(client_welcome)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send(IP.encode(ENCODING))
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
            print("Server is close")
            break
        elif command == "LOGOUT":
            # Disconnect from server
            print(f"{IP} is disconnecting")
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
            if file_name != "":
                print("Syntax Error")
                continue
            client.send(f"{command}".encode(ENCODING))
        elif command == "HELP":
            # Print the guildline
            print("ADD$<file_name>: add new file from repository to server")
            print("DELETE$<file_name>: delete file from server")
            print("LOGOUT: disconnect to server")
            print("CLOSE: disconnect and close the server")
            print("DOWNLOAD$<file_name>$<client's IP>")
            print("LIST: list all the file which the server can reach")
        else:
            print("Syntax Error")
        
    client.send(command.encode(ENCODING))
    os._exit(os.EX_OK)

        




if __name__ == "__main__":
    main()
