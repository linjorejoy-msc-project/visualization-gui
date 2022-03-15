import socket

from typing import List


class ConfigData:
    def __init__(
        self,
        id: str,
        name: str,
        subscribed_topics: List[str],
        published_topics: List[str],
        constants_required: List[str],
        variables_subscribed: List[str],
    ) -> None:
        self.id = id
        self.name = name
        self.subscribed_topics = subscribed_topics
        self.published_topics = published_topics
        self.constants_required = constants_required
        self.variables_subscribed = variables_subscribed


class Client:
    def __init__(
        self,
        client_socket: socket.socket,
        address: socket._Address,
        config_data: ConfigData,
    ) -> None:
        self.client_socket = client_socket
        self.address = address
        self.config_data = config_data


class ClientList:
    def __init__(self) -> None:
        self.clients: List[Client] = []

    def add_client(self, client: Client):
        self.clients.append(client)

    def remove_client(self, client: Client):
        self.clients.remove(client)
