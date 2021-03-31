from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)

print("UDP Client")

data = "UDP message"
sock.sendto(data.encode(), ("localhost", 5555))
