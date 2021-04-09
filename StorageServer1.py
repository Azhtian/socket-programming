import json
from socket import socket, create_server, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from select import select
from datetime import datetime
from getpass import getpass
import mysql.connector


def create_dataBase(db_name):
    my_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")


def determine_database(station_name):
    if station_name.upper() == "OSLO":
        return "east"
    else:
        return "west"


def create_table(station_name):
    db_name = determine_database(station_name)
    my_cursor.execute(f"USE {db_name};")
    my_cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {station_name} (DATA_TIME timestamp PRIMARY KEY, temperature LONGTEXT, precipitation VARCHAR(10));"
    )
    print(f"table created with the name: {station_name}")


def putMessage(data: str) -> None:
    # Puts the message into the corresponding table
    station_name, DATA_TIME, temperature, precipitation = data.split(",")
    # precipitation = precipitation.strip("\n")
    DATA_TIME = datetime.strptime(DATA_TIME, "%d/%m/%Y %H:%M:%S")
    # temp= float(temperature)
    db_name = determine_database(station_name)
    my_cursor.execute(f"USE {db_name};")
    my_cursor.execute(
        f"INSERT  INTO {station_name} VALUES ('{DATA_TIME}','{temperature}','{precipitation}');"
    )
    SQL_storage.commit()


def get(loc, entire: str) -> bytes:
    if entire == "whole":
        return get_all(loc)
    elif entire == "last":
        return get_last(loc)


def get_all(loc):
    db_name = determine_database(loc)
    # my_cursor.execute(f"USE {db_name};")
    my_cursor.execute(f"SELECT * FROM {db_name}.{loc};")
    data = my_cursor.fetchall()
    print(data)
    return data


def get_last(loc):
    db_name = determine_database(loc)
    # my_cursor.execute(f"USE {db_name};")
    my_cursor.execute(
        f"SELECT * FROM {db_name}.{loc} WHERE DATA_TIME = (SELECT MAX(DATA_TIME) FROM {db_name}.{loc}) ;"
    )

    data = my_cursor.fetchall()
    return data


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


def connect_udp(sock):
    data, address = sock.recvfrom(2048)
    message = data.decode()
    if message[0:3] == "ctb":
        create_table(message[4:].upper())
    else:
        putMessage(message)


def connect_tcp(sock):
    conn, address = sock.accept()
    print("accepted", conn, "from", address)
    message = conn.recv(2048).decode()

    loc, req = message.split(";")

    available_data = get(loc, req)

    for data in available_data:
        conn.sendall(f"Location: {loc} Time: {data[0]} temperature: {data[1]} precipitation: {data[2]} ".encode())


if __name__ == '__main__':

    # password = print("enter password for connect database: ")
    # password = getpass()
    SQL_storage = mysql.connector.connect(host='localhost', user='root', password="Sql96685204")
    my_cursor = SQL_storage.cursor()
    my_cursor.execute(f"CREATE DATABASE IF NOT EXISTS west")
    my_cursor.execute(f"CREATE DATABASE IF NOT EXISTS east")

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
