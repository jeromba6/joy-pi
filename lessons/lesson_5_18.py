#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read 16 button matrix

Position of switches:
+---+--------+--------+
|on |12345678|        |
|off|        |        |
+---+-----------------+
"""

import RPi.GPIO as GPIO
import time

class ButtonMatrix():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        #set IDs of the buttons
        self.buttonIDs = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]

        #declarate GPIO pins for the lines
        self.rowPins = [13,15,29,31]

        #declarate GPIO pins for the columns
        self.columnPins = [22,37,35,33]

        self.button = {}
        for col in range(4):
            for row in range(4):
                self.button[ col + 1 + 4 * row] = [self.rowPins[row], self.columnPins[col]]

        #define 4 inputs with pull up resistors
        for i in range(len(self.rowPins)):
            GPIO.setup(self.rowPins[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

        #define 4 outputs ans set them on high
        for j in range(len(self.columnPins)):
            GPIO.setup(self.columnPins[j], GPIO.OUT)
            GPIO.output(self.columnPins[j], 1)

    def activateButton(self, rowPin, colPin):
        #get button number
        btnIndex = self.buttonIDs[rowPin][colPin] - 1
        print("button " + str(btnIndex + 1) + " pressed")

        #prevent several presses on a button in a short time
        time.sleep(.3)

    def buttonHeldDown(self,pin):
        if(GPIO.input(self.rowPins[pin]) == 0):
             return True
        return False

def main():
    #initialisation of button matrix
    buttons = ButtonMatrix()
    try:
        while True:
            for j in range(len(buttons.columnPins)):

                #every output pin is set on low
                GPIO.output(buttons.columnPins[j],0)
                for i in range(len(buttons.rowPins)):
                    if GPIO.input(buttons.rowPins[i]) == 0:
                        buttons.activateButton(i,j)
            
                        #do nothing as long as teh button is pressed
                        while(buttons.buttonHeldDown(i)):
                            pass
                GPIO.output(buttons.columnPins[j],1)
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()