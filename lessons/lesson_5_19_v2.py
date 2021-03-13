#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Read IR sensor

Position of switches:
+---+--------+--------+
|on |        |        |
|off|        |        |
+---+-----------------+
"""

import RPi.GPIO as GPIO
import IRModule
import time

def remote_callback(code, p):
    n=8
    codebin=str(bin(code))[2:]
    codebin=[codebin[i:i+n] for i in range(0, len(codebin), n)]
    print('Hex code: {} bin: {} P: {}'.format(hex(code),codebin,p))
    time.sleep(1)
    remote_send(irPinOut, code)
    return

def remote_send(pin, code):
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    pulse_length = 0.0005
    n=1
    codebin=str(bin(code))[2:]
    codebin=[int(codebin[i:i+n]) for i in range(0, len(codebin), n)]
    for v in codebin:
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(pulse_length + pulse_length * 3 * v )
        GPIO.output(pin,GPIO.LOW)
        time.sleep(pulse_length)


# set up IR pi pin and IR remote object
irPin = 20
irPinOut = 26
ir = IRModule.IRRemote(callback='DECODE')
# using 'DECODE' option for callback will print out
# the IR code received in hexadecimal
# this can used to get the codes for whichever NEC
# compatable remote you are using

# set up GPIO options and set callback function required
# by the IR remote module (ir.pWidth)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)      # uses numbering outside circles
GPIO.setup(irPin,GPIO.IN)   # set irPin to input
GPIO.add_event_detect(irPin,GPIO.BOTH,callback=ir.pWidth)

ir.set_verbose() # verbose option prints outs high and low width durations (ms)
print('Starting IR remote sensing using DECODE function and verbose setting equal True ')
print('Use ctrl-c to exit program')

try:
    #time.sleep(5)

    # turn off verbose option and change callback function
    # to the function created above - remote_callback()
    print('Turning off verbose setting and setting up callback')
    ir.set_verbose(False)
    ir.set_callback(remote_callback)

    # This is where you could do other stuff
    # Blink a light, turn a motor, run a webserver
    # count sheep or mine bitcoin

    while True:
        time.sleep(1)

except:
    print('Removing callback and cleaning up GPIO')
    ir.remove_callback()
    GPIO.cleanup(irPin)