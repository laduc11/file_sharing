import socket
import os
import tqdm


# def create_file():
#     with open("client_data/data.txt", "w") as file:
#         for i in range(1000000):
#             file.write("Hello world\n")

# # create_file()
# # os._exit(os.EX_OK)

# IP = socket.gethostbyname(socket.gethostname())
# PORT = 16607
# ADDR = (IP, PORT)
# SIZE = 1024

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# for i in range(1):
#     try:
#         client.connect(ADDR)
#     except WindowsError as er:
#         if er.errno == 10056:
#             print('Socket is already connected.')
#         os._exit(os.EX_OK)

#     client.send("CONNECT$SUCCESS".encode())


# file_size = 0
# while True:
#     msg = client.recv(SIZE).decode()
#     msg = msg.split('$')

#     if msg[0] == "OK":
#         done = False
#         data = b""
#         progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=file_size)
#         while not done:
#             data += client.recv(SIZE)
#             progress.update(SIZE)
#             if data[-5:] == b"<END>":
#                 done = True
#                 data = data[:-5]
        
#         with open('server/data/meo.txt', 'wb') as file:
#             file.write(data)
        
#         break
    
#     elif msg[0] == "SIZE":
#         file_size = int(msg[1])
#         client.send("OK".encode())

# file_path = "E:/STM32/st-stm32cubeide_1.7.0_10852_20210715_0634_x86_64.exe"
# size = os.path.getsize(file_path)
# progress = tqdm.tqdm(desc="Hello", total=size, ncols=30)

role = input("Are you admin or client? ")
while role != "admin" and role != "client":
    role = input("Are you admin or client? ")



