import socket
import json
from helperfunctions.logger import add_log
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
    add_log(
        "INFO", f"Server in {socketKind} in host {hostName} at port {port} is started"
    )
    return new_socket


def on_new_client(client_socket: socket.socket, addr, iterations=5):

    client_socket.send(
        bytes(
            f"{len(INFO_TO_NEW_CLIENT_STR):<{HEADERSIZE}}" + INFO_TO_NEW_CLIENT, "utf-8"
        )
    )
    config_msg_len = int(client_socket.recv(HEADERSIZE))
    config_msg = client_socket.recv(config_msg_len)

    return config_msg
    # new_msg = True

    # data = ""
    # while True:
    # msg_len = client_socket.recv(HEADERSIZE)
    # if msg_len:
    #     data = client_socket.recv(int(msg_len))
    #     return data
    # else:
    #     return None
    # iterations -= 1
    # if iterations <= 0:
    #     return
    # time.sleep(1)
    # on_new_client(client_socket, addr, iterations)
    # break
    # if new_msg:
    #     msg_len = client_socket.recv(HEADERSIZE)
    #     if msg_len:
    #         print(f"Here {msg_len=}")
    #         msg_len = int(msg_len)
    #         add_log(
    #             "INFO", f"Data from {client_socket} of Length {msg_len} expected"
    #         )
    #         print(f"Found msg Len : {msg_len}")
    #         new_msg = False
    # else:
    #     data += client_socket.recv(BUFFERSIZE).decode("utf-8")
    # if len(data) == msg_len:
    #     add_log("INFO", f"Server Received : {data}")
    #     print(f"{data=}")
    #     return
