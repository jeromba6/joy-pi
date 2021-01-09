#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Control LED matrix

Position of switches:
+---+--------+--------+
|on |        |        |
|off|        |        |
+---+-----------------+

Positive values rotate counterclockwise
Negative values rotate clockwise
"""
import re
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


def main(cascaded, block_orientation, rotate):

    # Initialize LED matrix
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation,
    rotate=rotate or 0)

    # Output to console Matrix is initialized
    print("[-] Matrix initialized")

    # Define text
    msg = "Hello World! :-)"

    # Print text to console
    print("[-] Printing: {}".format(msg))

    # Print text to Matrix
    show_message(device, msg, fill="blue", font=proportional(CP437_FONT), scroll_delay=0.1)


if __name__ == "__main__":

    # cascaded = Number of MAX7219 LED Matrix's connected, standard=1
    # block_orientation = choices 0, 90, -90, standard=0
    # rotate = choices 0, 1, 2, 3, Rotate display 0=0°, 1=90°, 2=180°, 3=270°, standard=0

    try:
        main(cascaded=1, block_orientation=90, rotate=0)
    except KeyboardInterrupt:
        pass
