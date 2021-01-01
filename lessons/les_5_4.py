#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Vibrate for on relay for 1 second

Position of switches:
+---+--------+--------+
|on |        |1       |
|off|        |        |
+---+-----------------+
"""

import RPi.GPIO as GPIO
import time

vibrate_time = 1

# define vibration pin
vibration_pin = 13
# Set board mode to GPIO.BOARD
GPIO.setmode(GPIO.BOARD)
# Setup vibration pin to OUTPUT
GPIO.setup(vibration_pin, GPIO.OUT)
# turn on vibration
GPIO.output(vibration_pin, GPIO.HIGH)
# wait
time.sleep(vibrate_time)
# turn off vibration
GPIO.output(vibration_pin, GPIO.LOW)
# cleanup GPIO
GPIO.cleanup()