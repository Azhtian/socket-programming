from datetime import datetime
from time import sleep
from station import *
from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)

Bergen_station = StationSimulator(simulation_interval=1)
Bergen_station.turn_on()
sock.sendto(f"ctb {Bergen_station.location} ".encode(), ("localhost", 8800))
for _ in range(10):
    sleep(1)
    print("sending new data")
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sock.sendto(
        f"{Bergen_station.location},{time}, {Bergen_station.temperature}, {Bergen_station.rain}".encode(),("localhost", 8800)
    )

Bergen_station.shut_down()
