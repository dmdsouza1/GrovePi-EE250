import sys

import paho.mqtt.client as mqtt
import threading
import queue

from influxdb import InfluxDBClient
from datetime import datetime
import time
sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

import grovepi
from grovepi import *
LIGHT_STATUS = 0
hostname = "dmdsouza"
end_thread = False
# Using the queue library to lock the thread and add to or remove from the queue
q = queue.Queue()
control_light_queue = queue.Queue()
raw_light_data_queue = queue.Queue()

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe(hostname + "/led") #subscribing to the topic LED that is used to control the LED
    client.message_callback_add(hostname + "/led", led_callback)  #custom callback for topic led
    
def led_callback(client, userdata, message):
    message_recv = str(message.payload, "utf-8")
    if(message_recv == "LED_ON"):
        try:
            # adding the command to the queue
            print ("LED ON!")
            control_light_queue.put(1)
            time.sleep(0.2)
        except:             # Handles errors
            time.sleep(0.2)                             

    elif(message_recv == "LED_OFF"):
        try:
            # adding the command to the queue
            print ("LED OFF!")
            control_light_queue.put(0)
            time.sleep(0.2)
        except:             # Handles errors
            time.sleep(0.2)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

light_status_number = 0
def influx_thread(name):

    while True:
        if end_thread:
            break 
        try:  
            if q.empty():
                continue   
            #getting the light status and the raw light data from the queues 
            light_status_number = q.get() 
            raw_light_data = raw_light_data_queue.get()  
            # to get the most recent value from the queue we keep removing from front until the queue is empty
            while q.empty() != True:
                light_status_number = q.get()
                q.task_done()
                raw_light_data = raw_light_data_queue.get()
                raw_light_data_queue.task_done()

            # Gets time to enter in influxDB
            timeStr = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            json_body = [
                    {
                        "measurement": "light",            
                        "time": timeStr,
                        "fields": {                
                            "light_status": light_status_number,
                            "raw_light_data": raw_light_data
                        }
                    }
                ]

            client = InfluxDBClient(host = 'daniel-HP-Notebook', port = 8086, username = 'admin', password = 'password', database = 'test_light', ssl = True)
            client.write_points(json_body)
            # thread collects data every 10 seconds
            q.task_done()
            raw_light_data_queue.task_done()
            time.sleep(10)
            
        except KeyboardInterrupt:
            break




client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
client.loop_start()
# thread to handle all influxDB operations
influx = threading.Thread(target = influx_thread, daemon = True, args=(1,))
influx.start()

ULTRASONIC_PORT = 4     # D4
LIGHT_SENSOR = 1    #A1
LED_PORT = 2 # D2

light_threshold = 300
ultrasonic_threshold = 20
resistance = 0
sensor_value = 1

# Using a weighted average to get the sensor data
# The first, second, third index has the weights 0.25, 0.5, 0.25 respectively
light_sensor_window = [0,0,0]

weighted_sensor_value = 0.0

index = 0
higher_weight_index = 1
# Setup
grovepi.pinMode(ULTRASONIC_PORT, "INPUT")
grovepi.pinMode(LIGHT_SENSOR,"INPUT")
grovepi.pinMode(LED_PORT,"OUTPUT")
# turning on the light initially
digitalWrite(LED_PORT,1)

time.sleep(0.5)

while True:
    try:
        # controlling the light command
        if control_light_queue.empty() == False:
             item = control_light_queue.get()
             digitalWrite(LED_PORT,item)
             time.sleep(0.2)
             control_light_queue.task_done()
        if(index == 3):
            index = 0
        if(higher_weight_index == 3):
            higher_weight_index = 0
        ultrasonic_sensor_value = grovepi.ultrasonicRead(ULTRASONIC_PORT)
        time.sleep(0.2)
        sensor_value = grovepi.analogRead(LIGHT_SENSOR)
        if(sensor_value == 0):
            sensor_value = 1
        # Using resistance to get more precision for the light sensor values
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        # if 0 in light_sensor_window:
        #     light_sensor_window[0] = resistance
        #     light_sensor_window[1] = resistance
        #     light_sensor_window[2] = resistance
        light_sensor_window[index] = resistance
        # calculating the weighted average
        for i in range(3):
            if(i == higher_weight_index):
                # weighted_ultrasonic_value += ultrasonic_sensor_window[i] * 0.5
                weighted_sensor_value += light_sensor_window[i] * 0.5
            else:
                # weighted_ultrasonic_value += ultrasonic_sensor_window[i] * 0.25
                weighted_sensor_value += light_sensor_window[i] * 0.25

        print("raw ultrasonic value", ultrasonic_sensor_value)
        print("weighted sensor value", weighted_sensor_value)
        if(weighted_sensor_value < light_threshold):
            q.put(1)
            raw_light_data_queue.put(sensor_value)
            print("changed status to on")
        else:
            q.put(0)
            raw_light_data_queue.put(sensor_value)
            print("changed status to off")
        # publishing the raw ultrasonic data for processing
        client.publish(hostname + "/ultrasonic", str(ultrasonic_sensor_value))
        index += 1
        higher_weight_index += 1

        weighted_sensor_value = 0
        weighted_ultrasonic_value = 0
        time.sleep(1)

    except KeyboardInterrupt: 
        # Turning off the led before you exit
        digitalWrite(LED_PORT,0)  
        time.sleep(0.3)
        control_light_queue.join()
        q.join()
        raw_light_data_queue.join()
        end_thread = True     
        break

    except IOError:
            print ("Error")

    except ZeroDivisionError:
            pass




