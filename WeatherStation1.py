from datetime import datetime
from time import sleep
from station import *
from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)

Bergen_station = StationSimulator(simulation_interval=1)
Bergen_station.turn_on()
sock.sendto(f"ctb {Bergen_station.location} ".encode(), ("localhost", 8800))

Oslo_station = StationSimulator(location="Oslo", simulation_interval=1)
Oslo_station.turn_on()
sock.sendto(f"ctb {Oslo_station.location} ".encode(), ("localhost", 8800))

Stavanger_station = StationSimulator(location="Stavanger", simulation_interval=1)
Stavanger_station.turn_on()
sock.sendto(f"ctb {Stavanger_station.location} ".encode(), ("localhost", 8800))


for _ in range(20):
    sleep(1)
    print("sending new data")
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sock.sendto(
        f"{Bergen_station.location},{time}, {Bergen_station.temperature}, {Bergen_station.rain}".encode(),
        ("localhost", 8800)
    )
    sleep(1)
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sock.sendto(
        f"{Oslo_station.location},{time}, {Oslo_station.temperature}, {Oslo_station.rain}".encode(),
        ("localhost", 8800)
    )
    sleep(1)
    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sock.sendto(
        f"{Stavanger_station.location},{time}, {Stavanger_station.temperature}, {Stavanger_station.rain}".encode(),
        ("localhost", 8800)
    )

Bergen_station.shut_down()
Oslo_station.shut_down()
Stavanger_station.shut_down()
