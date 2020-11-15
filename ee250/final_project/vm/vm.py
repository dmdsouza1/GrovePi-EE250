from flask import Flask, jsonify
from flask import request
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

hostname = "dmdsouza"

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    # client.subscribe(hostname + "/lightcommand")
    # client.message_callback_add(hostname + "/lightcommand", lightcommand_callback) 


app = Flask(__name__)

@app.route('/')
def home():
    return "WELCOME TO THE LIGHT CONTROLLER"

@app.route('/lightstatus')
def lightstatus():
	
	result = client_influx.query('select light_status from light')
	LIGHT_STATUS = ""
	light_points = list(result.get_points(measurement='light'))
	# print(cpu_points)
	# getting the most recent data value from influxdb
	most_recent = light_points.pop()
	# print(most_recent)
	if most_recent["light_status"] == 1:
		LIGHT_STATUS = "ON"
	elif most_recent["light_status"] == 0:
		LIGHT_STATUS = "OFF"
	else:
		LIGHT_STATUS = "No data recorded"
	return jsonify(LIGHT_STATUS)

@app.route('/lightcommand')
def lightcommand():
	light_command = request.args.get('command')
	if light_command == "ON":
		client.publish(hostname + "/led", "LED_ON")
		return jsonify("Turning ON LED")
	elif light_command == "OFF":
		client.publish(hostname + "/led", "LED_OFF")
		return jsonify("Turning OFF LED")
	else:
		if light_command == None:
			return jsonify("Invalid Arguments in URL: [USAGE:/lightcommand?command=\"<ON or OFF>\"]")
		else:
			return jsonify("invalid argument")
	# except:
	# 	return "Invalid Arguments in URL: [USAGE:/lightcommand?command=\"<ON or OFF>\""


if __name__ == '__main__':
	client = mqtt.Client()
	client.on_connect = on_connect
	client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
	client.loop_start()
	client_influx = InfluxDBClient(host = 'localhost', port = 8086, username = 'admin1', password = 'password', database = 'test_light', ssl = True)
	app.run(debug=True, host='0.0.0.0')