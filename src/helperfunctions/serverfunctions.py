import socket


def start_server(
    addressFamily=socket.AF_INET,
    socketKind=socket.SOCK_STREAM,
    hostName=socket.gethostname(),
    port: int = 1234,
):
    new_socket = socket.socket(addressFamily, socketKind)
    new_socket.bind((hostName, port))
    print(f"Server in {socketKind} in host {hostName} at port {port} is started")
    return new_socket
