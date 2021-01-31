#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Detect distance with ultrasonic sensor

Position of switches:
+---+--------+--------+
|on |        |        |
|off|        |        |
+---+-----------------+
"""

import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BOARD) #set GPIO board configuration

# Declartation of variables
TRIG = 36
ECHO = 32

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
print ("Wait for signal to be clean.")
time.sleep(2) #wait 2 seconds
print ("Start messuring")

try:
    while True:
        GPIO.output(TRIG, True) #start sending ultrasonic signal
        time.sleep(0.00001) #waits 0.00001 seconds
        GPIO.output(TRIG, False) #stops sending a signal
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start #calculation for duration of pulse
        distance = pulse_duration * 17150 #calculation for determining distance
        distance = round(distance, 2) #solution is rounded to 2 decimal place
        print ("Distance:",distance,"cm")
        time.sleep(.5)
except KeyboardInterrupt:
    GPIO.cleanup() #enable GPIO ports again