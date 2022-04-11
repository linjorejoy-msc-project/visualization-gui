import socket
import threading
from typing import List

from helperfunctions.serverfunctions2 import (
    format_msg_with_header,
    recv_msg,
    start_server,
)


server_socket: socket.socket = start_server(port=1235)

client_sockets: List[socket.socket] = []


def broadcast(from_socket: socket.socket, info):
    global client_sockets
    for each_socket in client_sockets:
        if each_socket is not from_socket:
            each_socket.send(format_msg_with_header(info))


def handle_client(cl_socket: socket.socket, addr):
    while True:
        info = recv_msg(cl_socket)
        if info:
            broadcast(cl_socket, info)


def start_listening():
    global client_sockets
    while True:
        cl_socket, addr = server_socket.accept()
        client_sockets.append(cl_socket)
        new_thread = threading.Thread(
            target=handle_client,
            args=(
                cl_socket,
                addr,
            ),
        )
        new_thread.start()


def main():
    start_listening()


if __name__ == "__main__":
    main()
