#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hmc5883
from time import sleep

if __name__ == "__main__":

    # create instace
    debug_level = 1
    c = hmc5883.hmc5883(debug_level)

    # get bias
    c.calibration()

    # loop
    while 1:
        d  = c.get_bearing()
        print "Bearing: ", d
        sleep(1)
