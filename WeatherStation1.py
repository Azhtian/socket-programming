from datetime import datetime
from time import sleep
from station import *
from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)

station = StationSimulator(simulation_interval=1)
station.turn_on()

for _ in range(10):
    sleep(1)
    print("sending new data")
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sock.sendto(f"Station: {station.location } Time: {time}, temperature: {station.temperature}, precipitation: {station.rain}".encode(),
                ("localhost", 8800))


station.shut_down()
