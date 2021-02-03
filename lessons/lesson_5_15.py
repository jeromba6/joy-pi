#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control 7 segement display

Position of switches:
+---+--------+--------+
|on |        |        |
|off|        |        |
+---+-----------------+
"""

import time
import datetime
from Adafruit_LED_Backpack import SevenSegment

segment = SevenSegment.SevenSegment(address=0x70)

#segment of I2C address 0x70 and assign the display definition
segment.begin()

#intialisation of the display, must be performed once before the display can be used
print ("CTRL+C to end.")

def back_and_forth( value, positions ):
    mod_value = value % ( positions - 1 )
    direction1 = int( value / (positions - 1) ) % 2
    direction2 = 1 - (2 * direction1)
    return (direction1 * ( positions - 1 )) + direction2 * mod_value

#loop which permanently updates the time and shows on the display
try:
    nr_of_segments = 4
    while True:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        segment.clear()

        # display for the hours
        print(nr_of_segments)
        segment.set_digit(0, int(hour / 10),   0 == back_and_forth(second, nr_of_segments ))
        segment.set_digit(1, hour % 10,        1 == back_and_forth(second, nr_of_segments ))
        # display for the minutes
        segment.set_digit(2, int(minute / 10), 2 == back_and_forth(second, nr_of_segments ))
        segment.set_digit(3, minute % 10,      3 == back_and_forth(second, nr_of_segments ))

        print("Seconds: {:>2}, Dot: {}".format(second,back_and_forth(second, nr_of_segments )))
        # blink colon as seperator
        segment.set_colon(second % 2)
        segment.write_display() #is needed to update LEDs
        time.sleep(1) #wait one second
except KeyboardInterrupt:
    segment.clear()
    segment.write_display()