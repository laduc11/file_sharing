import socket
import os
import threading


IP = socket.gethostbyname(socket.gethostname())
PORT = 16607
ADDR = (IP, PORT)
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

def print_Hello():
    print("Hello")


# try:
#     temp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     temp.connect(ADDR)
# except Exception:
#     print("Can not connect to the server")

# [(1, 2, 3), ("")]
data = [("a", "b", "c"), ("1", "2", "3")]
result = ""
print(data)
for a in data:
    result += ' '.join(a) + '\n'
print(result)