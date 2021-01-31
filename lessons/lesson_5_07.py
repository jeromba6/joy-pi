#!/usr/bin/env python3

"""
Detect tempratue and humidity

Position of switches:
+---+--------+--------+
|on |        |        |
|off|        |        |
+---+-----------------+
"""

# needs 'sudo apt install gpiod libgpiod-dev'
# needs 'pip3 install adafruit-circuitpython-dht'

import sys
import adafruit_dht
import time
import datetime

# set pin number
pin = 4

# Define sensor
dht_device = adafruit_dht.DHT11(pin)

# Define interval
interval = 2

# Continues loop
while True:

    try:
        temperature = dht_device.temperature
        # Uncomment next line when you want temperature in Fahrenheit, default is Celcius as it should be ;-)
        # temperature = (temperature * 9 / 5) + 32

        # Uncomment next line when you want temperature in Fahrenheit, default is Celcius as it should be ;-)
        # temperature = temperature  + 273.15

        humidity = dht_device.humidity
        print('Time: {2} Temp={0:0.1f}* Humidity={1:0.1f}%'.format(temperature, humidity, datetime.datetime.now()))
    except:
        print('Failed to get reading. Try again!')
    time.sleep(interval)
