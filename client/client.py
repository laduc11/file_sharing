from client_lib import *

        
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_thread = threading.Thread(target=client_mode,args=(client,))
    client_thread.start()

    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_mode(host)

if __name__ == "__main__":
    main()
