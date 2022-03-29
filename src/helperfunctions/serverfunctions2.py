import socket
import json
from typing import List


from helpermodules.constants import HEADERSIZE
from helpermodules.RequiredObjects import ConfigData, DDSInfo, Participant


def start_server(
    addressFamily=socket.AF_INET,
    socketKind=socket.SOCK_STREAM,
    hostName=socket.gethostname(),
    port: int = 1234,
):
    new_socket = socket.socket(addressFamily, socketKind)
    new_socket.bind((hostName, port))
    new_socket.listen(5)
    return new_socket

# Helper Functions
def format_msg_with_header(msg: str, header_size: int = HEADERSIZE):
    return bytes(f"{len(msg):<{header_size}}" + msg, "utf-8")


def recv_msg(participant_socket: socket.socket) -> str:
    try:
        msg_len = int(participant_socket.recv(HEADERSIZE))
        return participant_socket.recv(msg_len).decode("utf-8")
    except Exception as e:
        print(f"Error Occured\n{e}")
        return None
