#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Detect distance with ultrasonic sensor

Position of switches:
+---+--------+--------+
|on |        |        |
|off|        |        |
+---+-----------------+
"""

import time
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd

# Define LCD nr of characters per line and nr of lines.
lcd_columns = 16
lcd_rows    = 2

# Setup I2C Bus
i2c = busio.I2C(board.SCL, board.SDA)

# Define lcd in variable
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, 0x21)

try:
    # turn backlight on
    lcd.backlight = True

    # Print 2 words
    lcd.message = "Hello\nWorld!"

    # Wait 5 seconds
    time.sleep(5.0)

    # Show cursor
    lcd.clear()
    lcd.cursor = True
    lcd.message = "Show Cursor!"

    # Wait 5 seconds
    time.sleep(5.0)

    # Flash cursor
    lcd.clear()
    lcd.blink = True
    lcd.message = "Blinky Cursor!"

    # Wait 5 seconds
    time.sleep(5)
    lcd.blink = False

    # Scroll message from left to right and back
    lcd.clear()
    scroll_msg = "<-- Scroll -->"
    lcd.message = scroll_msg
    for i in range(len(scroll_msg)):
        time.sleep(0.5)
        lcd.move_right()
    for i in range(len(scroll_msg)):
        time.sleep(0.5)
        lcd.move_left()

    # Flash backlight
    for wait in range(5, 0, -1):
        # lcd.clear()
        lcd.message = "Flash backlight\nin {} seconds...".format(wait)
        time.sleep(1.0)

    # Disable backlight
    lcd.backlight = False
    lcd.clear()
    lcd.message = "Flashing"
    time.sleep(1.0)
    lcd.backlight = True
    time.sleep(1.0)
    lcd.backlight = False

    # Say goodbye
    lcd.clear()
    lcd.message = "Goodbye"
    lcd.backlight = True
    time.sleep(2.0)

    # Hintergrundbeleuchtung ausschalten.
    lcd.clear()
    lcd.backlight = False

except KeyboardInterrupt:
    # LCD ausschalten.
    lcd.clear()
    lcd.backlight = False