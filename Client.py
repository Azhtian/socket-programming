from socket import create_connection, socket, AF_INET, SOCK_STREAM


def run() -> []:
    sock = create_connection(("localhost", 8888))
    print("Available locations:\n Oslo, Bergen, Stavanger....\n")
    loc = input("Choose location: ").upper()

    print("Would you like to see whole weather forecast or just last update? \n whole/last ")
    request = input(">")
    if request.lower().startswith("w"):
        sock.send(f"{loc};whole".encode())
    elif request.lower().startswith("l"):
        sock.send(f"{loc};last".encode())
    else:
        print("Invalid request!")

    elements = []

    while data := sock.recv(1024):
        print(data.decode())
        elements.append(data.decode())

    sock.close()
    return elements

run()

