import socket
import os
import threading
import time


IP = socket.gethostbyname(socket.gethostname())
PORT = 16607
IP_DST = "10.0.188.88"
ADDR = (IP_DST, PORT)
MY_ADDR = (IP, PORT)
ENCODING = "utf-8"
SIZE = 1024


# Wait another client connect
def wait_connect(client):
    client.bind(MY_ADDR)
    client.listen()
    print(f"Host {MY_ADDR} is listening")
    conn, addr = client.accept()
    data = conn.recv(SIZE).decode(ENCODING)     # Syntax: IP$host_name
    data = data.split('$')
    addr = (data[0], addr[1])
    conn.send(f"Hello {addr} from {MY_ADDR}".encode(ENCODING))

    while True:
        data = conn.recv(SIZE).decode(ENCODING)
        if data == "LOGOUT":
            conn.send("DISCONNECTED$".encode(ENCODING))
            print(f"{data}")
            break
        else: 
            conn.send("Syntax Error".encode(ENCODING))

    conn.close()

def client_mode(host):
    try:
        host.connect(ADDR)
    except Exception:
        print("Can not connect to server")
        exit()

    host.send(f"{IP}${socket.gethostname}".encode(ENCODING))
    while True:
        data = host.recv(SIZE).decode(ENCODING)
        print(data)
        command = input(">>> ")
        host.send(f"{command}".encode(ENCODING))
        if command == "LOGOUT":
            break

def test_multithread():
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    thread1= threading.Thread(target=wait_connect, args=(host,))
    thread1.start()

    thread2= threading.Thread(target=client_mode, args=(client,))
    thread2.start()

    print("Success")

# s = "Be Dipz dang iu\n"
# s =list(s)
# del s[-1]
# s = ''.join(s)
# print(type(s))


def host_mode():
    pass


def main():
    host = socket.socket()
    client = socket.socket()

    host_thread = threading.Thread(target=host_mode,args=(host,))
    client_thread = threading.Thread(target=client_mode,args=(client,))

    host_thread.start()
    client_thread.start()


def raise_timeout():
    raise TimeoutError

# data = b"1234567890"
# print(data)
# data = data[:-5]
# print(data)
# os._exit(os.EX_OK)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(MY_ADDR)
server.listen()
print("Server is listening")
client, addr = server.accept()

while True:
    msg = client.recv(SIZE).decode(ENCODING)
    msg = msg.split('$')

    if msg[0] == "CONNECT":
        client.send(f"SIZE${str(os.path.getsize('client_data/data.txt'))}".encode())
    elif msg[0] == "OK":
        client.send("OK".encode(ENCODING))
        time.sleep(0.05)
        file_data = open('client_data/data.txt', 'rb').read() + b"<END>"
        client.sendall(file_data)
        print("Send successfully")


