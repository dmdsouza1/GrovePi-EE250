GITHUB REPO : https://github.com/dmdsouza1/GrovePi-EE250.git

SHA 76891f3c9a0390ba9b8314600da6bc9f9870eaa8

NO TEAM MEMBERS

VIDEO LINK: 
 
The final_project is divided into two folders
The first folder contains the code to run on the rpi called rpi.py
The second folder contains the code to run on the node(Laptop). The signal_processing.py and vm.py runs on two separate terminals to increase readability of the output statements.

The RPI requires a light sensor, an LED and Ultrasonic sensor connected to A1, D2, D4 respectively

In this demo, due to constrains of access to hardware, we are assuming the ultrasonic sensor is in a hallway 
before the entrance of the door as shown in the final project writeup figure 1 and figure 2.

This project also assumes the required INFLUXDB and GRAFANA setup was made
Instructions are in the following link: https://docs.google.com/document/d/1oSitf82AZqWe7a0lVMXsFCsULKMTmgmPX2X7QaP95MY/edit
Please complete steps 3, 4.1, 4.2, 4.3, 4.5 and 5 

This project uses python3 flask, paho mqtt, and influxdb libraries
Use the following commands to install them:
$ pip install Flask
$ pip install paho-mqtt

For influxDB, on Debian/Ubuntu, you can install it with this command:
$ sudo apt-get install python-influxdb


INFLUXDB to see the data being updated in real time every 10 seconds
$ influx -ssl -unsafeSsl -username 'admin' -password 'password'
> use test_light
> select * from light


