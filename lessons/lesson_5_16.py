#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Detect touch

Position of switches:
+---+--------+--------+
|on |        |        |
|off|        |        |
+---+-----------------+
"""

from RPi import GPIO
import signal

#set TOUCH pin 11 (declaration of variables).
TOUCH = 11

#create function setup_gpio
def setup_gpio():
    GPIO.setmode(GPIO.BOARD) #use GPIO pins like in the GPIO board schemata
    GPIO.setup(TOUCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def do_smt(channel):
    print("Touch detected")

def main():
    setup_gpio()
    try:
        GPIO.add_event_detect(TOUCH, GPIO.FALLING, callback=do_smt, bouncetime=200)
        signal.pause()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()