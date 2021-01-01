#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Buzzing when up is pushed

Position of switches:
+---+--------+--------+
|on |      7 |        |
|off|123456 8|12345678|
+---+-----------------+
"""

import RPi.GPIO as GPIO
import time

# configure both button and buzzer pins
button_pin = 37
buzzer_pin = 12

# set board mode to GPIO.BOARD
GPIO.setmode(GPIO.BOARD)

# setup button pin as input and buzzer pin as output
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)
try:
    while True:
        # check if button pressed
        if(GPIO.input(button_pin) == 0):
        # set buzzer on
            GPIO.output(buzzer_pin, GPIO.HIGH)
        else:
        # it's not pressed, set button off
            GPIO.output(buzzer_pin, GPIO.LOW)
except KeyboardInterrupt:
    GPIO.cleanup()