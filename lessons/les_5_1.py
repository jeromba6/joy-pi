#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time #import librarys
buzzer_pin = 12 #define buzzer pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer_pin, GPIO.OUT)
for i in range(4):
    # Make buzzer sound
    GPIO.output(buzzer_pin, GPIO.HIGH)
    #wait 0.5 seconds
    time.sleep(0.5)
    # Stop buzzer sound
    GPIO.output(buzzer_pin, GPIO.LOW)
    time.sleep(0.2)
GPIO.cleanup()