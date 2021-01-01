#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Switch on relay for 1.5 second

Position of switches:
+---+--------+--------+
|on |        |        |
|off|        |        |
+---+-----------------+
"""

import RPi.GPIO as GPIO
import time

# Time the relay should be turned on
interval = 1.5

# define relay pin
relay_pin = 40
# set GPIO mode as GPIO.BOARD
GPIO.setmode(GPIO.BOARD)
# setup relay pin as OUTPUT
GPIO.setup(relay_pin, GPIO.OUT)
# Open Relay
GPIO.output(relay_pin, GPIO.LOW)
# Wait half a second
time.sleep(interval)
# Close Relay
GPIO.output(relay_pin, GPIO.HIGH)
GPIO.cleanup()