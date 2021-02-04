#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Detect tilt left right

Position of switches:
+---+--------+--------+
|on |        | 2      |
|off|        |        |
+---+-----------------+
"""

import time
import RPi.GPIO as GPIO

#define tilt_pin
tilt_pin = 15

#set GPIO mode to GPIO.BOARD
GPIO.setmode(GPIO.BOARD)

# set pin as INPUT
GPIO.setup(tilt_pin, GPIO.IN)

try:
    while True:
        #positive is tilt to the left / negative is tilt to the right
        if GPIO.input(tilt_pin):
            print ("[-] Left Tilt")
        else:
            print ("[-] Right Tilt")
        time.sleep(1)
except KeyboardInterrupt:
    #CTRL+C exists program
    GPIO.cleanup()