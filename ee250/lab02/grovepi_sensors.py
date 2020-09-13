""" EE 250L Lab 02: GrovePi Sensors

https://github.com/dmdsouza1/GrovePi-EE250

"""

"""python3 interpreters in Ubuntu (and other linux distros) will look in a 
default set of directories for modules when a program tries to `import` one. 
Examples of some default directories are (but not limited to):
  /usr/lib/python3.5
  /usr/local/lib/python3.5/dist-packages

The `sys` module, however, is a builtin that is written in and compiled in C for
performance. Because of this, you will not find this in the default directories.
"""
import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

import grovepi
from grove_rgb_lcd import *

# This if-statement checks if you are running this python file directly. That 
# is, if you run `python3 grovepi_sensors.py` in terminal, this if-statement will 
# be true

if __name__ == '__main__':
    SLIDE = 0   # A0
    PORT = 4    # D4
    previous_sensor_value = -1
    previous_ultrasonic_value = -1

    time.sleep(1)
    setRGB(0,255,0)
    setText(" ")

    while True:

        #So we do not poll the sensors too quickly which may introduce noise,
        #sleep for a reasonable time of 200ms between each iteration.
        time.sleep(0.2)
        try: 
            #reading in the potentiometer value from A0
            sensor_value = grovepi.analogRead(SLIDE)
            #reading in the ultrasonic reading value from D4
            ultrasonic_value = grovepi.ultrasonicRead(PORT)

            if(sensor_value >= ultrasonic_value ):
                setRGB(0,128,64)            
                setText_norefresh("{}cm OBJ PRES \n{}cm".format(str(sensor_value),str(ultrasonic_value)))

            elif(sensor_value < ultrasonic_value ):
                setRGB(0,255,0)
                setText_norefresh("{}cm          \n{}cm".format(str(sensor_value),str(ultrasonic_value)))
            
        except IOError:
            print("Error")
