import socket
import json
import time

# from helperfunctions.logger import add_log
from helpermodules.constants import BUFFERSIZE, HEADERSIZE

INFO_TO_NEW_CLIENT = {
    "headersize": 5,
}
INFO_TO_NEW_CLIENT_STR = json.dumps(INFO_TO_NEW_CLIENT)


def start_server(
    addressFamily=socket.AF_INET,
    socketKind=socket.SOCK_STREAM,
    hostName=socket.gethostname(),
    port: int = 1234,
):
    new_socket = socket.socket(addressFamily, socketKind)
    new_socket.bind((hostName, port))
    new_socket.listen(5)
    # add_log(
    #     "INFO", f"Server in {socketKind} in host {hostName} at port {port} is started"
    # )
    return new_socket


def send_server_config(participant_socket: socket.socket):
    global INFO_TO_NEW_CLIENT_STR

    config_msg = f"{len(INFO_TO_NEW_CLIENT_STR):<{HEADERSIZE}}" + INFO_TO_NEW_CLIENT_STR

    participant_socket.send(bytes(config_msg, "utf-8"))


def on_new_participant(participant_socket: socket.socket, addr, iterations=5):

    print("Waiting to receive length")
    participant_config_msg_len = participant_socket.recv(HEADERSIZE)
    print(f"Received len {participant_config_msg_len=}")
    participant_config_msg_len = int(participant_config_msg_len)
    print("Waiting to receive msg")
    participant_config_msg = participant_socket.recv(participant_config_msg_len)
    print("Received msg")

    config_msg = f"{len(INFO_TO_NEW_CLIENT_STR):<{HEADERSIZE}}" + INFO_TO_NEW_CLIENT_STR
    print(f"{config_msg=}")
    participant_socket.send(
        bytes(
            config_msg,
            "utf-8",
        )
    )
    print("Sent Config...")

    return participant_config_msg
