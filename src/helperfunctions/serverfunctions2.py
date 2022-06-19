import socket
import json
from typing import List


from helpermodules.constants import HEADERSIZE
from helpermodules.RequiredObjects import ConfigData, DDSInfo, Participant


def start_server(
    addressFamily=socket.AF_INET,
    socketKind=socket.SOCK_STREAM,
    hostName=socket.gethostname(),
    port: int = 1235,
):
    new_socket = socket.socket(addressFamily, socketKind)
    new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    new_socket.bind((hostName, port))
    new_socket.listen(5)
    return new_socket


# Helper Functions
def format_msg_with_header(msg: str, header_size: int = HEADERSIZE):
    return bytes(f"{len(msg):<{header_size}}" + msg, "utf-8")


def recv_msg(participant_socket: socket.socket) -> str:
    while True:
        len_str = participant_socket.recv(HEADERSIZE)
        if len_str:
            msg_len = int(len_str)
            return_str = participant_socket.recv(msg_len).decode("utf-8")
            if return_str:
                return return_str
