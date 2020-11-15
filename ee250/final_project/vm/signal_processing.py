import paho.mqtt.client as mqtt
import time
import queue
import threading

hostname = "dmdsouza"
count = 0
threshold_average = 0
q = queue.Queue()

data_array = queue.Queue()
number_of_people = 0



def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe(hostname + "/ultrasonic")
    client.message_callback_add(hostname + "/ultrasonic", lightcommand_callback) 

def lightcommand_callback(client, userdata, message):
    message_recv = str(message.payload, "utf-8")
    global count
    count += 1
    print("messsage: ", message_recv)
    q.put(int(message_recv))
    data_array.put(int(message_recv))


def detect_event(name):
    global number_of_people
    global threshold_average
    slice_data = [0,0,0,0,0,0,0,0,0]
    index = 0
    c = 0
    # Initializing the threshold value with 20 values of data
    while True:
        # getting a threshold value
        if c >= 20:
            break
        print("The number of people:", number_of_people)
        item = q.get()
        threshold_average = int((threshold_average * count + item) / (count + 1))
        print("threshold average:", threshold_average)
        q.task_done()
        test_item = data_array.get()
        data_array.task_done()
        c += 1
    c = 0
    i = 0
    person_detected = False
    while True:
        # gets ultrasonic data from queue
        ultrasonic_data = data_array.get()
        # if the data is less than half the threshold
        if ultrasonic_data < threshold_average // 2:
            # start adding the elements to the slice data array
            print("Detected an event")
            if i < 9:
                slice_data[i] = ultrasonic_data
                print("Slice data is ", slice_data[i])
                i += 1
            c += 1
            person_detected = True
            data_array.task_done()
            continue
        data_array.task_done()
        if c >= 10 and person_detected:
            print("entered the direction detection")
            print ("the slice data is****", slice_data)
            # if the slice data has less than three data points ignore the event
            if slice_data[0] == 0 or slice_data[1] == 0 or slice_data[2] == 0:
                c = 0
                i = 0
                person_detected = False
                slice_data = [0,0,0,0,0,0,0,0,0]
                continue
            # if the last index is a 0 
            if slice_data[8] == 0:
                # get the last index of actual data
                last_index = slice_data.index(0)
                # if the data is increasing then a person is leaving the room
                if slice_data[0] <= slice_data[last_index-1]:
                    number_of_people -= 1
                    print("The number of people:", number_of_people)
                # if the data is decreasing then a person is entering the room
                elif slice_data[0] >= slice_data[last_index-1]:
                    number_of_people += 1
                    print("The number of people:", number_of_people)
            else:
                # if the data is increasing then a person is leaving the room
                if slice_data[0] <= slice_data[8]:
                    number_of_people -= 1
                    print("The number of people:", number_of_people)
                # if the data is decreasing then a person is entering the room
                elif slice_data[0] >= slice_data[8]:
                    print("incremented1")
                    number_of_people += 1  
                    print("The number of people:", number_of_people)
            
            c = 0
            i = 0
            person_detected = False
            slice_data = [0,0,0,0,0,0,0,0,0]
        else:
            c += 1

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


    #this section is covered in publisher_and_subscriber_example.py
    # turn-on the worker thread
x = threading.Thread(target=detect_event, daemon=True, args = (1,))
x.start()
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
client.loop_start()
# create a thread 

while True:
    time.sleep(4)