from datetime import datetime
from time import sleep
from station import *
from socket import socket, AF_INET, SOCK_DGRAM

class WeatherStation: #A WeatherStation is a station and a socket with some desirable methods
    def __init__(self, location: str, sock: socket):
        self.station = StationSimulator(location=location, simulation_interval=1)
        self.sock = sock

    def turnOn(self):
        self.station.turn_on()

    def createDatabase(self):
        self.sock.sendto(f"ctb {self.station.location}".encode(), ("localhost", 8800))

    def sendData(self):
        #print(f"{self.station.location},{time}, {self.station.temperature}, {self.station.rain}") #DebugPrint
        self.sock.sendto(
            f"{self.station.location},{time}, {self.station.temperature}, {self.station.rain}".encode(),
            ("localhost", 8800))

    def startWeatherStation(self):
        self.station.turn_on()
        self.createDatabase()

def getTime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

if __name__ == '__main__':
    sock = socket(AF_INET, SOCK_DGRAM)

    Bergen_station = WeatherStation("Bergen", sock)
    Bergen_station.startWeatherStation()
    Oslo_station = WeatherStation("Oslo", sock)
    Oslo_station.startWeatherStation()
    Stavanger_station = WeatherStation("Stavanger", sock)
    Stavanger_station.startWeatherStation()

    for _ in range(20):
        print("sending new data")
        sleep(1)
        time = getTime()
        Bergen_station.sendData()
        sleep(1)
        time = getTime()
        Oslo_station.sendData()
        sleep(1)
        time = getTime()
        Stavanger_station.sendData()

    Bergen_station.station.shut_down()
    Oslo_station.station.shut_down()
    Stavanger_station.station.shut_down()