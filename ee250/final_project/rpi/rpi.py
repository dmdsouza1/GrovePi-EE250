import requests
import sys
import time


sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

import grovepi
import grove_rgb_lcd as lcd

ULTRASONIC_PORT = 4     # D4
LIGHT_SENSOR = 1    #A1

light_threshold = 100
ultrasonic_threshold = 20
resistance = 0
sensor_value = 1
LIGHT_STATUS = "off"
NUMBER_OF_PEOPLE_IN_ROOM = 0
light_sensor_window = [0,0,0]
ultrasonic_sensor_window = [0,0,0]
weighted_sensor_value = 0.0
weighted_ultrasonic_value = 0.0
index = 0
higher_weight_index = 1
# Setup
grovepi.pinMode(ULTRASONIC_PORT, "INPUT")
grovepi.pinMode(LIGHT_SENSOR,"INPUT")
#getting initial values for the windows
time.sleep(0.5)
print("hello")
'''
ultrasonic_sensor_window[0] = grovepi.ultrasonicRead(ULTRASONIC_PORT)  
time.sleep(0.2)
light_sensor_window[0] = sensor_value = grovepi.analogRead(LIGHT_SENSOR)
time.sleep(0.2)
ultrasonic_sensor_window[1] = grovepi.ultrasonicRead(ULTRASONIC_PORT)  
time.sleep(0.2)
light_sensor_window[1] = sensor_value = grovepi.analogRead(LIGHT_SENSOR)
time.sleep(0.2)
ultrasonic_sensor_window[2] = grovepi.ultrasonicRead(ULTRASONIC_PORT)  
time.sleep(0.2)
light_sensor_window[2] = sensor_value = grovepi.analogRead(LIGHT_SENSOR)
time.sleep(0.2)
time.sleep(0.5)
'''
print("entering while")
while True:
    try:
        print("in try")
        if(index == 3):
            index = 0
        if(higher_weight_index == 3):
            higher_weight_index = 0
        print("before read sensor")
        ultrasonic_sensor_window[index] = grovepi.ultrasonicRead(ULTRASONIC_PORT)
        time.sleep(1)
        sensor_value = grovepi.analogRead(LIGHT_SENSOR)
        if(sensor_value == 0):
            sensor_value = 1
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        light_sensor_window[index] = resistance
        for i in range(3):
            if(i == higher_weight_index):
                weighted_ultrasonic_value += ultrasonic_sensor_window[i] * 0.5
                weighted_sensor_value += light_sensor_window[i] * 0.5
            else:
                weighted_ultrasonic_value += ultrasonic_sensor_window[i] * 0.25
                weighted_sensor_value += light_sensor_window[i] * 0.25

        # if(resistance > threshold):
        #     print("light off")
        #     LIGHT_STATUS = "off"
        # else:
        #     print("light on")
        #     LIGHT_STATUS = "on"
        # calculating the weighted values

        print("weighted ultrasonic value", weighted_ultrasonic_value)
        print("weighted sensor value", weighted_sensor_value)
        index += 1
        higher_weight_index += 1
        weighted_sensor_value = 0
        weighted_ultrasonic_value = 0
        time.sleep(1)

    except KeyboardInterrupt:
        break

    except IOError:
            print ("Error")

    except ZeroDivisionError:
            pass



