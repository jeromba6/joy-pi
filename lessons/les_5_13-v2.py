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
}

button_released = {}
for button_name in button.keys():
   button_released[button_name] = True

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)
for button_name in button.keys():
   GPIO.setup(button[button_name], GPIO.IN, pull_up_down=GPIO.PUD_UP)

servo = GPIO.PWM(servo_pin, 350)
servo.start(0)
interval = 2
position = 70
p_position = position - 1
try:
   while True:
      for key in button_released.keys():
         if not button_released[key] and GPIO.input(button[key]):
            button_released[key] = True

      if GPIO.input(button['up']) == 0 and button_released['up']:
         button_released['up'] = False
         position += 10

      if GPIO.input(button['down']) == 0 and button_released['down']:
         button_released['down'] = False
         position -= 10
      if position > 100:
         position = 100
      if position < 0:
         position = 0
      if p_position != position:
         print(position)
         # servo.start(0)
         servo.ChangeDutyCycle(position)
         time.sleep(.2)
         # servo.stop()
         p_position = position
          # time.sleep(interval)
except KeyboardInterrupt:
    pass
servo.stop()
GPIO.cleanup()
