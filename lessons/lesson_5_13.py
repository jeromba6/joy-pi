#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control servo motor

Position of switches:
+---+--------+--------+
|on |        |       8|
|off|        |        |
+---+-----------------+

Positive values rotate counterclockwise
Negative values rotate clockwise
"""

import RPi.GPIO as GPIO
import time
import sys


class sg90:
    def __init__(self, pin: int):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
        self.pin = int(pin)
        self.direction = 0
        self.servo = GPIO.PWM(self.pin, 50)
        self.servo.start(0.0)

    def cleanup(self):  # Funktion zum Stoppen und GPIO Pins Freigeben
        self.servo.ChangeDutyCycle(self._henkan(0))
        time.sleep(0.3)
        self.servo.stop()
        GPIO.cleanup()

    # Funktion die die Momentane Position feststellt.
    def currentdirection(self):
        return self.direction

    def _henkan(self, value):
        return 0.05 * value + 7.0

    def setdirection(self, direction, speed):  # Funktion um die Richtung anzugeben

        for d in range(self.direction, direction, int(speed)):
            self.servo.ChangeDutyCycle(self._henkan(d))
            print(self._henkan(d))
            self.direction = d
            time.sleep(0.1)
        self.servo.ChangeDutyCycle(self._henkan(direction))
        self.direction = direction


def main():
    servo_pin = 22
    s = sg90(servo_pin)  # Deklaration von Pin und Motor
    try:
        while True:
            print("Turn left ...")
            s.setdirection(80, 100)  # Links Herum drehen
            time.sleep(0.5)  # 0,5 Sekunden warten
            s.setdirection(50, 100)  # Links Herum drehen
            time.sleep(0.5)  # 0,5 Sekunden warten
            s.setdirection(50, 100)  # Links Herum drehen
            time.sleep(0.5)  # 0,5 Sekunden warten
            print("Turn right ...")
            s.setdirection(-80, 100)  # Rechts Herum drehen
            time.sleep(01.5)  # 0,5 Sekunden warten
            s.setdirection(-50, 100)  # Rechts Herum drehen
            time.sleep(01.5)  # 0,5 Sekunden warten
    except KeyboardInterrupt:
        s.cleanup()


if __name__ == "__main__":
    main()
