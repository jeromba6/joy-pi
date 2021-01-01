#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Start buzzing when up is pushed
Stop buzzing when down is pushed
Faster buzzing when left is pushed
Slower buzzing when richt is pushed
Alternate buzzing with vibrating

Position of switches:
+---+--------+--------+
|on |    5678|1       |
|off|        |        |
+---+-----------------+
"""
import RPi.GPIO as GPIO
import time

# configure both button and buzzer pins
buzzer_pin = 12
vib_pin = 13
button = {
    'up':    37,
    'down':  33,
    'left':  22,
    'right': 35
}

# set board mode to GPIO.BOARD
GPIO.setmode(GPIO.BOARD)

# setup button pin as input and buzzer pin as output
GPIO.setup(button['up'],    GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button['down'],  GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button['left'],  GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button['right'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(vib_pin, GPIO.OUT)

button_released = {
    'up':    True,
    'down':  True,
    'left':  True,
    'right': True
}

buzzer_interval = 0.2
buzzer_lenght = 0.2
buzzer_state = False
buzz = False
buzzer_time = 0
try:
    while True:
        for key in button_released.keys():
            if not button_released[key] and GPIO.input(button[key]):
                button_released[key] = True
                print('Button: {} - Value: {} - Time: {}'.format(key,
                                                                 GPIO.input(button[key]), time.time()))

        # check if button up is pressed
        if GPIO.input(button['up']) == 0 and button_released['up']:
            button_released['up'] = False
            if not buzzer_state:
                buzzer_time = time.time()
                buzz = True
            buzzer_state = True

        # check if button down is pressed
        if GPIO.input(button['down']) == 0:
            GPIO.output(vib_pin, GPIO.LOW)
            buzzer_state = False
            buzz = False

        if GPIO.input(button['left']) == 0 and button_released['left']:
            button_released['left'] = False
            buzzer_interval = buzzer_interval * 0.9
            print('Faster: {}'.format(buzzer_interval))

        if GPIO.input(button['right']) == 0 and button_released['right']:
            button_released['right'] = False
            buzzer_interval = buzzer_interval * 1.1
            print('Slower: {}'.format(buzzer_interval))

        if buzzer_state:
            if buzz:
                if time.time() - buzzer_time > buzzer_lenght:
                    buzz = False
                    buzzer_time = time.time()
            else:
                if time.time() - buzzer_time > buzzer_interval:
                    buzz = True
                    buzzer_time = time.time()

        if buzz:
            GPIO.output(buzzer_pin, GPIO.HIGH)
            GPIO.output(vib_pin, GPIO.LOW)
        else:
            GPIO.output(buzzer_pin, GPIO.LOW)
            if buzzer_state:
                GPIO.output(vib_pin, GPIO.HIGH)
except KeyboardInterrupt:
    GPIO.output(buzzer_pin, GPIO.LOW)
    GPIO.cleanup()
