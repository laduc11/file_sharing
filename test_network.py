import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(socket.gethostname())
print(f"Your Computer IP Address is: {IPAddr}" )
