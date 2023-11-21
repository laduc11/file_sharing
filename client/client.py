import socket
import os

IP = socket.gethostbyname(socket.gethostname())
IP_ADDR = "10.0.189.56"
PORT = 5500
ADDR = (IP_ADDR, PORT)
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
        command = input("> ")
        command = command.split("$")

        if len(command) == 1:
            command = ''.join(command)
        elif len(command) == 2:
            command, file_name = command
        else:
            continue

        if command == "CLOSE":
            # Close server
            print("Server is close")
            break
        elif command == "LOGOUT":
            # Disconnect from server
            print(f"{IP} disconnected")
            break
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
            client.send(f"{command}${file_name}")
        else:
            print("Syntax error")
        
    client.send(command.encode(ENCODING))
    os._exit(os.EX_OK)

        




if __name__ == "__main__":
    main()
