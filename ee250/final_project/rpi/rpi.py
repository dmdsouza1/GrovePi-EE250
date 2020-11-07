import requests
import sys
import time

sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')



import math

from grovepi import *
from grove_oled import *

dht_sensor_port = 7     # Connect the DHt sensor to port 7

time.sleep(1)
print("hello")
while True:
    try:
        time.sleep(1)
        print("henlo")
        dht(dht_sensor_port,0)
        time.sleep(1)
        [ temp,hum ] = dht(dht_sensor_port,1)       #Get the temperature and Humidity from the DHT sensor
        if math.isnan(temp) or  math.isnan(humidity):
            [temp,humidity] = dht(dht_sensor_port,0)
            print('temperature ',temp, 'humidity ',humidity)

        time.sleep(.5)
        print("temp =", temp, "C\thumidity =", hum,"%") 
        time.sleep(1)   
    except (IOError,TypeError) as e:
        print("Error")