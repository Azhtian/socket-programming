from socket import socket, AF_INET, SOCK_DGRAM, create_server, timeout
from select import select

# Where weather data will be stored

udp_sock = socket(AF_INET, SOCK_DGRAM)


class StorageServer:

    def __init__(self):
        self._welcome_sock = create_server(("localhost", 5555))
        self._BUFFER_SIZE = 2048


