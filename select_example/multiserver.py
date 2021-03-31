from socket import socket, AF_INET, SOCK_DGRAM
from select import select

server_address = ("localhost", 5555)

udp_sock = socket(AF_INET, SOCK_DGRAM)
udp_sock.bind(server_address)

tcp_sock = socket()
tcp_sock.bind(server_address)
tcp_sock.listen()


def read_tcp(sock):
    conn, address = sock.accept()
    print("accepted", conn, "from", address)
    data = conn.recv(2048)
    conn.close()
    print(f"From TCP client: {data.decode()}")


def read_udp(sock):
    data, address = sock.recvfrom(2048)
    print(f"From UDP client {address}: {data.decode()}")


sockets = [tcp_sock, udp_sock]

while True:
    inputready, _, _ = select(sockets, [], [])
    for key in inputready:
        if key == tcp_sock:
            read_tcp(key)
        elif key == udp_sock:
            read_udp(key)
        else:
            print("unknown socket: ", key)

# Funnet fra https://stackoverflow.com/questions/5160980/use-select-to-listen-on-both-tcp-and-udp-message
