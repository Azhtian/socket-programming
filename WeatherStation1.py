import numpy
from time import sleep
from station import *
from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)

station = StationSimulator(simulation_interval=1)
station.turn_on()

temperature = []
precipitation = []

for _ in range(10):
    sleep(1)
    temperature.append(station.temperature)
    precipitation.append(station.rain)

station.shut_down()

print("Temperature\tPrecipitation")
for t, p in zip(temperature, precipitation):
    print(t, "\t\t", p)

data = f"First element in temperature: {temperature[0]}"
sock.sendto(data.encode(), ("localhost", 8888))

