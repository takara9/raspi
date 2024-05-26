#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
#

import RPi.GPIO as GPIO
import time
from datetime import datetime 
import math


class hscr05:
    def __init__(self, trig, echo, debug_level):
        self.trig = trig
        self.echo = echo
        self.t1 = 0
        self.t2 = 0
        self.dt = 0
        self.debug = debug_level

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)
        GPIO.output(self.trig, GPIO.LOW)
        time.sleep(0.3)


    def read(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        state = 0
        while state != 3:
            if GPIO.input(self.echo) == 0 and state == 0:
                state = 1
            if GPIO.input(self.echo) == 1 and state == 1:
                self.t1 = datetime.now()
                state = 2
            if GPIO.input(self.echo) == 0 and state == 2:
                self.t2 = datetime.now()
                state = 3

        self.dt = self.t2 - self.t1
        usec = self.dt.microseconds
        self.dist = usec / 58
        if self.debug > 1:
            print "RESPONSE TIME = %5.0f uSec" % usec
            print "DISTANCE %3.1f cm" % self.dist
        return self.dist


    def cleanup(self):
        GPIO.cleanup()

    def scan(self):
        retry = 1
        while 1:
            scan = []
            sum = 0
            num = 3
            dev = 0
            ave = 0
            max = 0
            min = 9999

            for i in range(num):
                rslt = self.read()
                scan.append(rslt)
                sum = sum + rslt
                if self.debug > 1:
                    print "scan =",i,"  rslt = ",rslt
                if max < rslt:
                    max = rslt
                if min > rslt:
                    min = rslt
                time.sleep(0.08)
            
            ave = sum/num
            dev = max - min
            d0 = 0
            for i in range(num):
                d0 = d0 + math.fabs(ave - scan[i])
                scan[i] = 0
            sdv = d0/num
            err = sdv / ave * 100

            if self.debug > 0:
                print "retry = %2d" % retry
                print "ave = %4.1f cm" % ave
                print "max = %4.1f cm" % max
                print "min = %4.1f cm" % min
                print "sdv = %4.1f cm" % sdv
                print "dev = %4.1f cm" % dev 
                print "err = %3d %%" % err

            if err < 10:
                return ave
            else:
                retry += 1
                if retry > 3:
                    return -1
                time.sleep(0.3)
            

if __name__ == "__main__":
    pass

