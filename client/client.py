from client_lib import *

        
def main():
    # Get IP address of server
    server_ip = input("IP address of server = ")
    while not is_ip_valid(server_ip):
        server_ip = input("IP address of server = ")
    role = input("Are you admin or client? ")
    while role != "admin" and role != "client":
        role = input("Are you admin or client? ")

    is_admin = False
    if role == "admin":
        is_admin = True
    

    # Run client mode
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_thread = threading.Thread(target=client_mode, args=(client, server_ip, is_admin))
    client_thread.start()

    # Run host mode
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_mode(host)

if __name__ == "__main__":
    main()
