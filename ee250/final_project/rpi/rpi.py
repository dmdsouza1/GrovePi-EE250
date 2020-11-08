import requests
import sys
import time

sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

import grovepi
import grove_rgb_lcd as lcd

ULTRASONIC_PORT = 4     # D4
LIGHT_SENSOR = 1    #A1

threshold = 100
resistance = 0
sensor_value = 1
LIGHT_STATUS = "off"


# Setup
grovepi.pinMode(ULTRASONIC_PORT, "INPUT")
grovepi.pinMode(LIGHT_SENSOR,"INPUT")

time.sleep(1)
while True:
    try:
        time.sleep(0.2)
        # sensor_value = grovepi.analogRead(LIGHT_SENSOR)
        
        ultrasonic_value = grovepi.ultrasonicRead(ULTRASONIC_PORT)
         
        time.sleep(0.1)     
        
        if (resistance < threshold):
            pass
        
        sensor_value = grovepi.analogRead(LIGHT_SENSOR)
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        if(resistance == 0):
            resistance += 1
        time.sleep(0.1)
        if(resistance > threshold):
            print("light off")
            LIGHT_STATUS = "off"
        else:
            print("light on")
            LIGHT_STATUS = "on"
        print("ultrasonic value", ultrasonic_value)

    except KeyboardInterrupt:
        break

    except IOError:
            print ("Error")

    except ZeroDivisionError:
            pass



