from socket import socket, AF_INET, SOCK_STREAM

sock = socket(AF_INET, SOCK_STREAM)

print("TCP Client")

sock.connect(("localhost", 5555))
data = "TCP message"
sock.send(data.encode())
sock.close()
