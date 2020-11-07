import requests
import sys
import time

sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

import grovepi
import grove_rgb_lcd as lcd

# Modules for my apps
import my_reddit
import my_weather
import my_space_station
#import my_app  # TODO: Create my_app.py using another API, following the examples as a template

ULTRASONIC_PORT = 4     # D4
LIGHT_SENSOR = 1    #A1

threshold = 10
resistance = 0
sensor_value = 1



# Setup
grovepi.pinMode(ULTRASONIC_PORT, "INPUT")
grovepi.pinMode(LIGHT_SENSOR,"INPUT")

time.sleep(1)
while True:
    try:
        time.sleep(0.2)
        # sensor_value = grovepi.analogRead(LIGHT_SENSOR)
        
        ultrasonic_value = grovepi.ultrasonicRead(PORT)
         
        time.sleep(0.1)     
        
        if (resistance < threshold):
            pass
            
        time.sleep(0.1)
        
        sensor_value = grovepi.analogRead(LIGHT_SENSOR)
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        time.sleep(0.1)
        print("light sensor value", resistance)
        print("ultrasonic value", ultrasonic_value)

    except KeyboardInterrupt:
        break

    except IOError:
            print ("Error")

    except ZeroDivisionError:
            pass



