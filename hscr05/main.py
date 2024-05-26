#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import hscr05
import math

hs = hscr05.hscr05(17,27,3)


if __name__ == "__main__":

    while 1:
        dist = hs.scan()
        print "Distance = %3d cm" % dist
        time.sleep(2)



