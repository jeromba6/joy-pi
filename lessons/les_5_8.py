#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import datetime

# define motion pin
motion_pin = 16

# set GPIO as GPIO.BOARD
GPIO.setmode(GPIO.BOARD)

# set pin mode as INPUT
GPIO.setup(motion_pin, GPIO.IN)

try:
    while True:
        if(GPIO.input(motion_pin) == 0):
            print "Nothing moves ..."
        elif(GPIO.input(motion_pin) == 1):
            print "Motion detected!"
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()