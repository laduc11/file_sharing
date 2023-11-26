from client_lib import *

        
def main():
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_mode(host)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_thread = threading.Thread(target=client_mode,args=(client,))
    client_thread.start()


if __name__ == "__main__":
    main()
