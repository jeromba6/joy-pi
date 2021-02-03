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
from Adafruit_LED_Backpack import SevenSegment

segment = SevenSegment.SevenSegment(address=0x70)

#segment of I2C address 0x70 and assign the display definition
segment.begin()

#intialisation of the display, must be performed once before the display can be used
print ("CTRL+C to end.")

#loop which permanently updates the time and shows on the display
try:
    nr_of_segments = 4
    pos1 = 0
    pos2 = 2
    s1 = 0
    s2 = 63
    s3 = 7
    s4 = 56
    while True:
        segment.clear()

        # display for the hours
        pos1 += 1
        if pos1 > 5: pos1 = 0
        pos2 += 1
        if pos2 > 5: pos2 = 0
        s1 = s1 ^ 2 ** pos1
        s2 = s2 ^ 2 ** pos1
        s3 = s3 ^ 2 ** pos2
        s4 = s4 ^ 2 ** pos2

        segment.set_digit_raw(0, s1)
        segment.set_digit_raw(1, s2)
        segment.set_digit_raw(2, s3)
        segment.set_digit_raw(3, s4)
        segment.set_colon(int(time.time()) % 2)
        segment.write_display() #is needed to update LEDs
        time.sleep(1) #wait one second
except KeyboardInterrupt:
    segment.clear()
    segment.write_display()