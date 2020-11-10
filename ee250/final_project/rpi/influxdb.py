from influxdb import InfluxDBClient
from datetime import datetime
import random
import time
random_num = random.randrange(0,100)
random_num = random_num



timeStr = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
print('time->',timeStr)

json_body = [
        {
            "measurement": "light",            
            "time": timeStr,
            "fields": {                
                "light_status": random_num
            }
        }
    ]

client = InfluxDBClient(host = 'https://daniel-HP-Notebook', port = 8086, username = 'admin', password = 'password', database = 'test_light', ssl = True)

result=client.write_points(json_body)
print(result)

time.sleep(3)
result = client.query('select light_status from light')

print("Result: {0}".format(result))

