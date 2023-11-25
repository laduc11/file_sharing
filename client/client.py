from client_lib import *

        
def main():
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_thread = threading.Thread(target=host_mode,args=(host,))
    client_thread = threading.Thread(target=client_mode,args=(client,))

    host_thread.start()
    client_thread.start()


if __name__ == "__main__":
    main()
