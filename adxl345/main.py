#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Device driver for ADXL345
# 3-axis accelerometer 
# 
# Reference documents
#  http://www.analog.com/media/jp/technical-documentation/data-sheets/ADXL345_jp.pdf
#
# 2016/12/29
# Maho Takara
#

import adxl345
from time   import sleep
import math


# Create instance
debug_level = 0
m = adxl345.adxl345(debug_level)

# Self Test
print "Self test result = ", m.selfTest()


# Calibration set bias
m.calibration()


# Loop
while 1:
    (ax,ay,az) = m.get_accel()
    print "Xaccel = %d" % ax
    print "Yaccel = %d" % ay
    print "Zaccel = %d" % az

    roll = math.degrees(math.atan2(ay,az))
    print "roll = %d deg" % roll

    pitch = math.degrees(math.atan2(ax,az))
    print "pitch = %d deg" % pitch
    print

    sleep(0.5)
