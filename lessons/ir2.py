#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import json

def main():
    ir_pin = 38
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(ir_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        print("Starting IR Listener")
        print("Waiting for signal")
        while True:
            code = get_ir(ir_pin)
            code_stats = stats(code)
            analyze(code)
            analyze2(code, code_stats)
            # print(code)


    except KeyboardInterrupt:
        pass
    except RuntimeError:
        # this gets thrown when control C gets pressed
        # because wait_for_edge doesn't properly pass this on
        pass
    print("Quitting")
    destroy()

def analyze2(code, code_stats):
    c0 = []
    c1 = []
    ct = []
    for c in code:
        if c[0]:
            c1.append(int(c[1]/code_stats['min_high']*10)/10)
        else:
            c0.append(int(c[1]/code_stats['min_low']*10)/10)
        ct.append(int(c[1]/code_stats['min']*10)/10)
    print(c1)
    print(len(c1))
    print(c0)
    print(len(c0))
    # print(ct)

def stats(code):
    code_stats = {'min': 1, 'max': 0,'min_low': 1, 'max_low': 0,'min_high': 1, 'max_high': 0, 'total': 0, 'total_high': 0, 'total_low': 0}
    for c in code:
        code_stats['min'] = min(code_stats['min'], c[1])
        code_stats['max'] = max(code_stats['max'], c[1])
        code_stats['total'] += c[1]
        if c[0]:
            code_stats['min_high'] = min(code_stats['min_high'], c[1])
            code_stats['max_high'] = max(code_stats['max_high'], c[1])
            code_stats['total_high'] += c[1]
        else:
            code_stats['min_low'] = min(code_stats['min_low'], c[1])
            code_stats['max_low'] = max(code_stats['max_low'], c[1])
            code_stats['total_low'] += c[1]

    code_stats['avg'] = code_stats['total'] / len(code)
    code_stats['avg_low'] = code_stats['total_low'] / (len(code) // 2)
    code_stats['avg_high'] = code_stats['total_low'] / ((len(code) + 1 ) // 2 )
    code_stats['count'] = len(code)
    return code_stats

def setup(pin):
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def get_ir(pin):
    t = time.time()
    received = []
    max_length = .5
    while GPIO.input(pin):
        t = time.time()
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
    main()
