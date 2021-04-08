from socket import create_connection, socket, AF_INET, SOCK_STREAM
sock= create_connection(("localhost", 8888))

print("Would you like to see whole weather forecast or just last update? \n whole/last ")
request = input(">")
if request.lower().startswith("w"):
    sock.send("whole".encode())
elif request.lower().startswith("l"):
    sock.send("last".encode())
else:
    print("Invalid request!")
data = sock.recv(2048)
print(data.decode())
sock.close()
