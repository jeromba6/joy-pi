#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

def setup(pin):
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def get_ir(pin):
    received = []
    t = time.time()
    max_length = .5
    while GPIO.input(pin):
        t = time.time()
    ts = t
    while time.time() - t < max_length:
        while not GPIO.input(pin) and time.time() -t < max_length:
            pass
        received.append([1, time.time()-t])
        t = time.time()
        while GPIO.input(pin) and time.time() -t < max_length:
            pass
        if time.time() -t < max_length:
            received.append([0, time.time()-t])
            t = time.time()
    return (received)


def analyze(code):
    one = []
    zero = []
    times=[]
    for c in code:
        # print(c)
        times.append(c[1])
        if not c[0]:
            one.append(c[1])
        else:
            zero.append(c[1])
    # print ('Zero avg: {}, max: {}, min: {}'.format(sum(zero)/len(zero),max(zero),min(zero)))
    # print(zero)
    # print ('One  avg: {}, max: {}, min: {}'.format(sum(one)/len(one),max(one),min(one)))
    # print(one)
    samp = times[4:20]
    avg = sum(samp)/len(samp)
    output = ''
    for i in range(len(one)):
        if i > 2 and zero[i] > avg:
            break
        if zero[i] < avg:
            output += str(int(one[i] > avg))
    print('Hex code: {}, bin: {}'.format(hex(int(output, 2)),output))

def destroy():
    GPIO.cleanup()


if __name__ == "__main__":
    ir_pin = 38
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(ir_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        print("Starting IR Listener")
        print("Waiting for signal")
        while True:
            code = get_ir(ir_pin)
            analyze(code)


    except KeyboardInterrupt:
        pass
    except RuntimeError:
        # this gets thrown when control C gets pressed
        # because wait_for_edge doesn't properly pass this on
        pass
    print("Quitting")
    destroy()