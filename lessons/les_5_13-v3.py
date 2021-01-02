#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control servo motor

Position of switches:
+---+--------+--------+
|on |        |      78|
|off|        |        |
+---+-----------------+
"""

import RPi.GPIO as GPIO
import time as time

servo_pin = 22
button = {
    'up':    37,
    'down':  33,
    'left':  22,
    'right': 35
}
button_released = {
    'up':    True,
    'down':  True,
    'left':  True,
    'right': True
}

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin,50)

for button_name in button.keys():
    GPIO.setup(button[button_name], GPIO.IN, pull_up_down=GPIO.PUD_UP)

servo.start(0)
interval = 2

position = 7

try:
   while True:
      p_position = position
      for key in button_released.keys():
         if not button_released[key] and GPIO.input(button[key]):
            button_released[key] = True

      if GPIO.input(button['up']) == 0 and button_released['up']:
         button_released['up'] = False
         position += 1

      if GPIO.input(button['down']) == 0 and button_released['down']:
         button_released['down'] = False
         position -= 1

      if position != p_position:
         print(position)
      servo.ChangeDutyCyle(position)

except KeyboardInterrupt:
   pass
servo.stop()
GPIO.cleanup()
