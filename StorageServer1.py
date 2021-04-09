from socket import socket, create_server, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from select import select
from datetime import datetime
from getpass import getpass
import mysql.connector


def create_dataBase(db_name):
    my_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")


def create_table(station_name):
    print(f"table created with the name: {station_name}")
    my_cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {station_name} (DATA_TIME timestamp PRIMARY KEY, temperature LONGTEXT, precipitation VARCHAR(10));")


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

    for data in available_data:
        conn.sendall(f"Time: {data[0]} temperature: {data[1]} precipitation: {data[2]}\n".encode())


def connect_udp(sock):
    data, address = sock.recvfrom(2048)
    put(data)


# Fetch data from text file
def get_from_file(entire: str) -> bytes:
    with open("storage.txt", "rb") as f:
        if entire == "last":
            lines = f.readlines()
            return lines[-1]
        else:
            return f.read()


def put_in_file(text: bytes) -> None:
    with open("storage.txt", "ab") as f:
        f.write(text + b"\n")


def get(entire: str) -> bytes:
    if entire == "whole":
        return get_all()
    elif entire == "last":
        return get_last()


def get_all():
    my_cursor.execute(f"SELECT * FROM weather.BERGEN;")
    data = my_cursor.fetchall()
    print(data)
    return data


def get_last():
    my_cursor.execute(
        f"SELECT * FROM WEATHER.Bergen WHERE DATA_TIME = (SELECT MAX(DATA_TIME) FROM WEATHER.Bergen) ;"
    )

    data = my_cursor.fetchall()
    print("last data: ", data)
    return data


def put(text: bytes) -> None:
    message = text.decode()
    if message[0:3] == "ctb":
        create_table(message[4:-1])
    else:
        putMessage(message)


def putMessage(data: str) -> None:
    # Puts the message into the corresponding table
    station_name, DATA_TIME, temperature, precipitation = data.split(",")

    DATA_TIME = datetime.strptime(DATA_TIME, "%d/%m/%Y %H:%M:%S")
    # temp= float(temperature)
    print(station_name + " ", DATA_TIME, " " + temperature + " " + precipitation)
    my_cursor.execute(
        f"INSERT  INTO {station_name} VALUES ('{DATA_TIME}','{temperature}','{precipitation}');"
    )
    SQL_storage.commit()

if __name__ == '__main__':
    # db_name = input("enter database name: ")
    # print("enter password for connect database: ")
    # password = input("enter password for connect database: ")
    # password = getpass()
    SQL_storage = mysql.connector.connect(host='localhost', user='root', password='rykkje1011', database='weather')
    my_cursor = SQL_storage.cursor()
    create_dataBase("weather")

    # Where weather data will be stored
    server_address = ("localhost", 8888)

    udp_sock = socket(AF_INET, SOCK_DGRAM)

    udp_sock.bind(("localhost", 8800))

    tcp_sock = socket()
    tcp_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcp_sock.bind(server_address)
    tcp_sock.listen()

    sockets = [tcp_sock, udp_sock]

    while True:
        input_ready, _, _ = select(sockets, [], [])
        for key in input_ready:
            if key == tcp_sock:
                connect_tcp(key)

            elif key == udp_sock:
                connect_udp(key)

            else:
                print("unknown socket: ", key)
