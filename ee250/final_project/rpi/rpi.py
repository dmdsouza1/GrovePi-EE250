import requests
import sys
import time

sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

import grovepi
import grove_rgb_lcd as lcd

import math

# Connect the Grove Temperature & Humidity Sensor Pro to digital port D4
# This example uses the blue colored sensor.
# SIG,NC,VCC,GND
sensor = 4  # The Sensor goes on digital port 4.

# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.

while True:
    try:
        # This example uses the blue colored sensor. 
        # The first parameter is the port, the second parameter is the type of sensor.
        print("stuck at dht")
        [temp,humidity] = grovepi.dht(sensor,blue)  
        print("still stuck at dht")
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
        else:
            print("nan values")
        time.sleep(0.5)

    except IOError:
        print ("Error")