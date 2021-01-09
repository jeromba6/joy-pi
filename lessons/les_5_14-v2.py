#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Color rendering demo.
"""

import time
import random
from luma.led_matrix.device import max7219
from luma.core.render import canvas
from luma.core.interface.serial import spi, noop
import RPi.GPIO as GPIO

buzzer_pin = 12
vib_pin = 13
button = {
    'up':    37,
    'down':  33,
    'left':  22,
    'right': 35
}
# set board mode to GPIO.BOARD
GPIO.setmode(GPIO.BOARD)

# setup button pin as input and buzzer pin as output
for button_name in button.keys():
    GPIO.setup(button[button_name], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(vib_pin, GPIO.OUT)

button_released = {
    'up':    True,
    'down':  True,
    'left':  True,
    'right': True
}


def main():
    vib = False
    buzz = False
    while True:
        game = Tic_Tac_Toe()
        player = 1
        interval = 2

        c = 0
        t = time.time()
        while not game.end():
            for key in button_released.keys():
                if not button_released[key] and GPIO.input(button[key]):
                    button_released[key] = True

            if GPIO.input(button['right']) == 0 and button_released['right']:
                button_released['right'] = False
                c += 1
                if c > 8:
                    c = 0

            if GPIO.input(button['left']) == 0 and button_released['left']:
                button_released['left'] = False
                c -= 1
                if c < 0:
                    c = 8

            if GPIO.input(button['up']) == 0 and button_released['up']:
                button_released['up'] = False
                if game.move(c%3,int(c/3),player):
                    GPIO.output(vib_pin, GPIO.HIGH)
                    vib = True
                    vib_end = time.time() + 0.1
                    if player == 2:
                        player = 1
                    else:
                        player = 2
                    # game.move(x,y,player)
                    print('#' * 9)
                    game.print()
                    print ('End: {}'.format(game.end()))
                else:
                    GPIO.output(buzzer_pin, GPIO.HIGH)
                    buzz = True
                    buzz_end = time.time() + 0.3
            if vib and vib_end < time.time():
                GPIO.output(vib_pin, GPIO.LOW)
                vib = False
            if buzz and buzz_end < time.time():
                GPIO.output(buzzer_pin, GPIO.LOW)
                buzz = False

            game.display(cursor_show = True, cursor_position = c)
    print('End of game, winner is: {}'.format(game.end()))


class Tic_Tac_Toe:

    def __init__(self):
        # set board
        self.board = [ [0,0,0],[0,0,0],[0,0,0] ]
        self.board_interval_on  = 1
        self.board_interval_off = 9
        self.board_draw_status = True
        self.board_draw_counter = 0
        self.cursor = 0
        self.cursor_interval = 0.5
        self.cursor_timer = time.time()

    def board_reset(self):
        self.board = [ [0,0,0],[0,0,0],[0,0,0] ]


    def end(self):
        winner = 0
        for x in range(3):
            if self.board[x][0] == self.board[x][1] == self.board[x][2] and self.board[x][0]:
                winner = self.board[x][0]
                break
            if self.board[0][x] == self.board[1][x] == self.board[2][x] and self.board[0][x]:
                winner = self.board[0][x]
                break
        if self.board[1][1]:
            if self.board[0][0] == self.board[1][1] == self.board[2][2]:
                winner = self.board[1][1]
            if self.board[2][0] == self.board[1][1] == self.board[0][2]:
                winner = self.board[1][1]
        return winner

    def standing(self):
        return self.board

    def print(self):
        for line in self.board:
            print(line)

    def move(self, x, y, v):
        if not self.board[y][x]:
            self.board[y][x] = v
            return True
        return False

    def display(self, cursor_show = False, cursor_position = 0):
        self.board_draw_counter += 1
        if self.board_draw_status:
            if self.board_draw_counter > self.board_interval_on:
                self.board_draw_status = False
                self.board_draw_counter = 0
        else:
            if self.board_draw_counter > self.board_interval_off:
                self.board_draw_status = True
                self.board_draw_counter = 0

        with canvas(device) as draw:
            # Draw board with interval so it will be darker
            if self.board_draw_status:
                draw.rectangle((2,0,2,7), fill=1)
                draw.rectangle((5,0,5,7), fill=1)
                draw.rectangle((0,2,7,2), fill=1)
                draw.rectangle((0,5,7,5), fill=1)

            # Draw pieces on the board
            for x in range(3):
                for y in range(3):
                    if self.board[y][x] == 1:
                        draw.point((x*3,y*3), fill=1)
                        draw.point((x*3+1,y*3+1), fill=1)
                    if self.board[y][x] == 2:
                        draw.point((x*3+1,y*3), fill=1)
                        draw.point((x*3,y*3+1), fill=1)

            # Draw cursor
            if cursor_show:
                if time.time() - self.cursor_timer > self.cursor_interval:
                    self.cursor_timer = time.time()
                    self.cursor += 1
                    if self.cursor > 3:
                        self.cursor = 0
                x = cursor_position % 3
                y = int(cursor_position/3)
                draw.point((x*3+int(self.cursor/2),y*3+(self.cursor%2)), fill=1)


if __name__ == "__main__":
    try:
        serial = spi(port=0, device=1, gpio=noop())
        device = max7219(serial, cascaded=1, block_orientation=90,
        rotate=0)
        main()
    except KeyboardInterrupt:
        GPIO.output(buzzer_pin, GPIO.LOW)
        GPIO.cleanup()
    GPIO.output(buzzer_pin, GPIO.LOW)
    GPIO.cleanup()
