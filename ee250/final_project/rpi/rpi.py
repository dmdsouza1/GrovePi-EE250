import sys

import paho.mqtt.client as mqtt
import threading

from influxdb import InfluxDBClient
from datetime import datetime
import random #don't need
import time
sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

import grovepi

LIGHT_STATUS = "off"
hostname = "dmdsouza"
lock = threading.Lock()

# def on_connect(client, userdata, flags, rc):
#     print("Connected to server (i.e., broker) with result code "+str(rc))
    # client.subscribe(hostname + "/led")
    # client.subscribe(hostname + "/lcd")
    # client.message_callback_add(hostname + "/led", led_callback)  #custom callback for topic led
    # client.message_callback_add(hostname + "/lcd", lcd_callback)  #custom callback for topic lcd

# def lcd_callback(client, userdata, message):
#     message_recv = str(message.payload, "utf-8")
#     #displaying w a s d according 
#     if(message_recv in lcd_list):
#         try:
#             if(message_recv == "w"):
#                 setText_norefresh("{}\n".format("w"))
#             elif(message_recv == "a"):
#                 setText_norefresh("{}\n".format("a"))
#             elif(message_recv == "s"):
#                 setText_norefresh("{}\n".format("s"))
#             elif(message_recv == "d"):
#                 setText_norefresh("{}\n".format("d"))
#         except:
#             time.sleep(0.2)
light_status_number = 0
def influx_thread(name):
    while True:        
        with lock:
            if(LIGHT_STATUS == "off"):
                light_status_number = 0
            else:
                light_status_number = 1

    


        timeStr = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


        json_body = [
                {
                    "measurement": "light",            
                    "time": timeStr,
                    "fields": {                
                        "light_status": light_status_number
                    }
                }
            ]

        client = InfluxDBClient(host = 'daniel-HP-Notebook', port = 8086, username = 'admin', password = 'password', database = 'test_light', ssl = True)
        result=client.write_points(json_body)
        time.sleep(10)



def grovepi_thread(name):
    ULTRASONIC_PORT = 4     # D4
    LIGHT_SENSOR = 1    #A1

    light_threshold = 100
    ultrasonic_threshold = 20
    resistance = 0
    sensor_value = 1
    
    NUMBER_OF_PEOPLE_IN_ROOM = 0
    light_sensor_window = [0,0,0]
    # ultrasonic_sensor_window = [0,0,0]
    weighted_sensor_value = 0.0
    # weighted_ultrasonic_value = 0.0
    index = 0
    higher_weight_index = 1
    # Setup
    grovepi.pinMode(ULTRASONIC_PORT, "INPUT")
    grovepi.pinMode(LIGHT_SENSOR,"INPUT")
    #getting initial values for the windows
    time.sleep(0.5)
    print("hello")
    while True:
        try:
            if(index == 3):
                index = 0
            if(higher_weight_index == 3):
                higher_weight_index = 0
            ultrasonic_sensor_value = grovepi.ultrasonicRead(ULTRASONIC_PORT)
            time.sleep(0.2)
            sensor_value = grovepi.analogRead(LIGHT_SENSOR)
            if(sensor_value == 0):
                sensor_value = 1
            resistance = (float)(1023 - sensor_value) * 10 / sensor_value
            light_sensor_window[index] = resistance
            for i in range(3):
                if(i == higher_weight_index):
                    # weighted_ultrasonic_value += ultrasonic_sensor_window[i] * 0.5
                    weighted_sensor_value += light_sensor_window[i] * 0.5
                else:
                    # weighted_ultrasonic_value += ultrasonic_sensor_window[i] * 0.25
                    weighted_sensor_value += light_sensor_window[i] * 0.25

            print("weighted ultrasonic value", ultrasonic_sensor_value)
            print("weighted sensor value", weighted_sensor_value)
            with lock:
                if(weighted_sensor_value < light_threshold):
                    LIGHT_STATUS = "on"
                    print("changed status to on")
                else:
                    LIGHT_STATUS = "off"
                    print("changed status to off")
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



if __name__ == '__main__':
    # client = mqtt.Client()
    # client.on_message = on_message
    # client.on_connect = on_connect
    # client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    # client.loop_start()
    influx = threading.Thread(target = influx_thread,args=(1,))
    influx.start()
    grovepi_threading =threading.Thread(target = grovepi_thread, args=(1,))
    grovepi_threading.start()
    while True:
        try:
            time.sleep(4)
        except KeyboardInterrupt:
            print("killing the threads")
            influx.kill()
            grovepi_threading.kill()
            break
   



