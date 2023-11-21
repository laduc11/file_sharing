import socket
import os
import threading

ENCODING = "utf-8"

def main():
    raw_data = "The server is online".encode(ENCODING)
    print(raw_data)
    print(raw_data.decode(ENCODING))

if __name__ == "__main__":
    main()