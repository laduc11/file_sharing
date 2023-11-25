import socket
import os
import threading

import file_manage as fm


# 10 Types of command receive
# Return message after processing the command
# CLOSE
def close_cmd():
    pass


# LOGOUT
def logout_cmd():
    pass


# DISCONNECTED
def disconnected_cmd():
    pass


# LOCAL
def local_cmd():
    pass


# ADD
def add_cmd():
    pass


# DELETE
def delete_cmd():
    pass


# LIST
def list_cmd():
    pass


# DOWNLOAD
def close_cmd():
    pass


# DISCOVERY
def discovery_cmd():
    pass


# PING
def ping_cmd():
    pass


# Process command and return reply message client
def process_command(command):
    pass

# Receive request from client and reply
def client_handle(client):
    pass


# Create server
def create_server(server):
    pass


# main function expected
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    create_server(server)