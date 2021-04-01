from socket import socket, create_server, AF_INET, SOCK_DGRAM
from select import select

# Where weather data will be stored
server_address = ("localhost", 8888)

udp_sock = socket(AF_INET, SOCK_DGRAM)

udp_sock.bind(("localhost", 8800))

tcp_sock = socket()
tcp_sock.bind(server_address)
tcp_sock.listen()


def connect_tcp(sock):
    conn, address = sock.accept()
    print("accepted", conn, "from", address)
    req = conn.recv(2048)

    available_data = get(req.decode())
    conn.sendall(available_data.encode())
    conn.close()
    #print(f"From TCP client: {data.decode()}")


def connect_udp(sock):
    data, address = sock.recvfrom(2048)
    put(data.decode())
    #print(f"From UDP client {address}: {data.decode()}")



def get(entire: str) -> str:
    with open("storage.txt", "r") as f:
        if entire == "last":
            lines = f.readlines()
            return lines[-1]
        else:
            return f.read()


def put(text: str) -> None:
    with open("storage.txt", "a") as f:
        f.write(text+"\n")


sockets = [tcp_sock, udp_sock]

while True:
    inputready, _, _ = select(sockets, [], [])
    for key in inputready:
        if key == tcp_sock:
            connect_tcp(key)

        elif key == udp_sock:
            connect_udp(key)

        else:
            print("unknown socket: ", key)


