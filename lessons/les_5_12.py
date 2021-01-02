#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control stepper motor

Position of switches:
+---+--------+--------+
|on |        |  3456  |
|off|        |        |
+---+-----------------+

Positive values rotate clockwise
Negative values rotate counterclockwise
"""

import time
import RPi.GPIO as GPIO
import math

class Stepmotor:

    def __init__(self):
        # set GPIO modus
        GPIO.setmode(GPIO.BOARD)

        # Pins connected to stepmotor
        self.pins = (29, 31, 33 ,35)
        self.interval = 0.002

        # Define pins as output and set default value
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

        self.Step_reset()

    def Step_reset(self):
        for pin in self.pins:
            GPIO.output(pin, False)

    def Step(self, direction):
        nr_of_steps = 8
        if direction < 0:
            start = 0
            stop  = nr_of_steps
            steps = 1
        else:
            start = nr_of_steps - 1
            stop  = -1
            steps = -1

        for step in range(start, stop, steps):
            m1 = int(step / 2)
            m2 = m1
            if step % 2:
                m2 = m1 + 1
                if m2 > 3:
                    m2 = 0
            GPIO.output(self.pins[m1], True)
            GPIO.output(self.pins[m2], True)
            time.sleep(self.interval)
            self.Step_reset()

    def turn(self,count):
        for loop in range(abs(int(count))):
            self.Step(count)

    def close(self):
        # Release GPIO
        GPIO.cleanup()

    def turnDegrees(self, count):
        # Rotate n degees
        self.turn(round(count*512/360,0))

    def turnDistance(self, dist, rad):
        # Rotate to travel x distance
        self.turn(round(512*dist/(2*math.pi*rad),0))

def main():
    motor = Stepmotor()

    print('Do 512 steps')
    motor.turn(512)

    print('Do -400 steps')
    motor.turn(-400)

    print("Turn 90 degrees")
    motor.turnDegrees(90)

    print("Turn -90 degerees")
    motor.turnDegrees(-90)

    print("Stop")
    motor.close()

if __name__ == "__main__":
    main()
