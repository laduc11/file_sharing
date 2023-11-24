import socket
import os
import threading

# from pythonping import ping


IP = socket.gethostbyname(socket.gethostname())
PORT = 16607
IP_DST = "10.0.188.88"
ADDR = (IP_DST, PORT)
MY_ADDR = (IP, PORT)
ENCODING = "utf-8"
SIZE = 1024

# hostname = socket.gethostname()
# IPAddr = socket.gethostbyname(socket.gethostname())
# print(f"Your Computer IP Address is: {IPAddr}" )

# data = "MinhDuc"
# data = data.split(" ")
# print(' '.join(os.listdir("client/")))
# # print(data[1])

# data = (5, 10)
# print(data[0])

# def print_Hello():
#     print("Hello")


# try:
#     temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     temp.connect(ADDR)
# except Exception:
#     print("Can not connect to the server")

# [(1, 2, 3), ("")]
# data = [("a", "b", "c"), ("1", "2", "3")]
# result = ""
# print(data)
# for a in data:
#     result += ' '.join(a) + '\n'
# print(result)

# my_list = []
# my_list += ["abc"] + ["def"]
# print(my_list)


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


# thread = threading.Timer(2.0, raise_timeout)
# thread.start()
# meo = input(">>> ")
# thread.cancel()
# print(meo)
file_name = "hai_ngoo.txt"
data = b"meo meo meo meo"
DATA_PATH = "client/data/"
with open(DATA_PATH + file_name, "wb") as download_file:
    download_file.write(data)