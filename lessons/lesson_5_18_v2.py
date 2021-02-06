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
        self.nrButtons = len(rowPins) * len(colPins)
        self.state_false = []
        self.state_true = []
        self.buttons_release_count = [0] * ( self.nrButtons + 1 )
        self.previousState={}
        for index in range(1,self.nrButtons + 1):
            self.previousState[index] = False

        self.state = self.buttonsState()
        self.previousState = self.state

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
            GPIO.output(self.columnPins[col],1)
        for col in range(len(self.columnPins)):
            GPIO.output(self.columnPins[col],0)
            for row in range(len(self.rowPins)):
                buttonNr = col + row * len( self.columnPins ) + 1
                state[buttonNr] = not GPIO.input(self.rowPins[row])

                # Next part is for correcting errors when the system thinks a button is released while this is not the case
                if state[buttonNr] != self.previousState[buttonNr] and self.previousState[buttonNr]:
                    self.buttons_release_count[buttonNr] += 1
                    if self.buttons_release_count[buttonNr] > 20:
                        self.buttons_release_count[buttonNr] = 0
                    else:
                        state[buttonNr] = self.previousState[buttonNr]
                else:
                    self.buttons_release_count[buttonNr] = 0
            GPIO.output(self.columnPins[col], 1)
        return dict(sorted(state.items()))

    def getButtonsState(self):
        self.previousState = self.state
        self.state = self.buttonsState()
        self.state_true = []
        self.state_false = []
        for button in range(1, self.nrButtons + 1):
            if self.state[button]:
                self.state_true.append(button)
            else:
                self.state_false.append(button)
        return self.state != self.previousState

def main():
    GPIO.setmode(GPIO.BOARD)

    #initialisation of button matrix
    buttons = ButtonMatrix([22,37,35,33],[13,15,29,31])
    # buttons2 = ButtonMatrix([37,35],[15,29])
    try:
        while(True):
            if buttons.getButtonsState():
                print('Changed buttons: {}'.format(buttons.changed()))
                print('Buttons status : {}'.format(buttons.state))
                print('Buttons True   : {}'.format(buttons.state_true))
                print('Buttons False  : {}'.format(buttons.state_false))
                print()
            # if buttons2.getButtonsState():
            #     print('Changed buttons2: {}'.format(buttons2.changed()))
            #     print('Buttons2 status: {}'.format(buttons2.show()))
            #     print()

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()