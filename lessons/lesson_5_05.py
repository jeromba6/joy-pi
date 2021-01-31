#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

"""
Detect sound

Position of switches:
+---+--------+--------+
|on |        |        |
|off|        |        |
+---+-----------------+
"""

# define sound pin
sound_pin = 18
# set GPIO mode to GPIO.BOARD
GPIO.setmode(GPIO.BOARD)
# setup pin as INPUT
GPIO.setup(sound_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
try:
    last = time.time()
    while True:
        # check if sound detected or not
        if(GPIO.input(sound_pin)==GPIO.LOW):
            print('Sound interval: {} - Detected at: {}'.format(time.time() - last, time.time()))
            last = time.time()
            time.sleep(0.5)
except KeyboardInterrupt:
    # CTRL+C detected, cleaning and quitting the script
    GPIO.cleanup()