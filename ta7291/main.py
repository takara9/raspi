#!/usr/bin/python
# -*- coding: utf-8 -*-

import ta7291
import time

if __name__ == "__main__":

    drv = ta7291.ta7291(21, 16, 20)

    print "Normal Power up and down"

    print "Ramp up"
    for power in range(0, 100, 10):
        drv.drive(power)
        time.sleep(5)

    print "Ramp down"
    for power in range(100, 0, -10):
        drv.drive(power)
        time.sleep(5)

    print "Stop 3 seconds..."
    drv.drive(0)
    time.sleep(3)

    print "Forward max speed, 3 seconds and brake..."
    drv.drive(100)
    time.sleep(3)
    drv.brake()
    time.sleep(1)

    print "Reverse max speed, 3 seconds and brake..."
    drv.drive(-100)
    time.sleep(3)
    drv.brake()
    time.sleep(1)

    print "close"
    drv.cleanup()


