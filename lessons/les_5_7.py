#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

import sys
import Adafruit_DHT
import time
import datetime

# set type of the sensor
sensor = 11

# set pin number
pin = 4

# Try to grab a sensor reading. Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32
# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print('Time: {2} Temp={0:0.1f}* Humidity={1:0.1f}%'.format(temperature, humidity, datetime.datetime.now().isoformat()))
    else:
        print('Failed to get reading. Try again!')
    time.sleep(1)
