#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read button matrix

Position of switches:
+---+--------+--------+
|on |12345678|        |
|off|        |        |
+---+-----------------+
"""

import RPi.GPIO as GPIO
import time

class ButtonMatrix():
    def __init__(self, colPins, rowPins):
        self.rowPins = rowPins
        self.columnPins = colPins
        self.state = self.buttonsState()
        self.previousState = self.state

    def show(self):
        return self.state

    def changed(self):
        changed = {}
        for button in self.state.keys():
            if self.state[button] != self.previousState[button]:
                changed[button] = self.state[button]
        return changed

    def buttonsState(self):
        state = {}
        for row in range(len(self.rowPins)):
            GPIO.setup(self.rowPins[row], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        for col in range(len(self.columnPins)):
            GPIO.setup(self.columnPins[col], GPIO.OUT)
            GPIO.output(self.columnPins[col], 1)
        for col in range(len(self.columnPins)):
            GPIO.output(self.columnPins[col], 0)
            for row in range(len(self.rowPins)):
                state[col + row * len( self.columnPins ) + 1] = GPIO.input(self.rowPins[row])
            GPIO.output(self.columnPins[col], 1)
        return state

    def getButtonsState(self):
        self.previousState = self.state
        self.state = self.buttonsState()
        return self.state != self.previousState

def main():
    GPIO.setmode(GPIO.BOARD)

    #initialisation of button matrix
    buttons = ButtonMatrix([22,37,35,33],[13,15,29,31])
    try:
        while(True):
            if buttons.getButtonsState():
                print('Changed buttons: {}'.format(buttons.changed()))
                print('Buttons status: {}'.format(buttons.show()))

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()