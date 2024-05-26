#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Driver module of HMC5883L
# Axis Digital Compass IC
# 
# Reference documents
#  https://cdn.sparkfun.com/datasheets/Sensors/Magneto/HMC5883L-FDS.pdf
#
# 2016/12/29
# Maho Takara
#

import os
import math
from smbus2 import SMBus # https://pypi.python.org/pypi/smbus2/0.1.4            
from time import sleep

# I2C
# slave address                                                                 
DEV_ADDR   = 0x1E

CONFIG_A   = 0x00
CONFIG_B   = 0x01
DEV_MODE   = 0x02
X_OUTPUT_H = 0x03
X_OUTPUT_L = 0x04
Z_OUTPUT_H = 0x05
Z_OUTPUT_L = 0x06
Y_OUTPUT_H = 0x07
Y_OUTPUT_L = 0x08
STATUS     = 0x09
IDENTIFY_A = 0x10
IDENTIFY_B = 0x11
IDENTIFY_C = 0x12

CALIB_FILE = 'hmc5883_calibration.dat'

# HMC5883L Class
class hmc5883():
    def __init__(self,debug):
        self.bus = SMBus(1)
        self.bus.write_byte_data(DEV_ADDR, 0, 0b01110000) # Set to 8 samples @ 15Hz
        self.bus.write_byte_data(DEV_ADDR, 1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
        self.bus.write_byte_data(DEV_ADDR, 2, 0b00000000) # Continuous sampling
        self.scale = 0.92    # Where is from?
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.z_offset = 0.0  # not using
        self.debug_level = debug

        # load calibration data if its exists
        if os.path.isfile(CALIB_FILE):
            f = open(CALIB_FILE,'r')
            dat = f.read()
            a = dat.splitlines()
            self.x_offset = int(a[0])
            self.y_offset = int(a[1])
            f.close()


    def calibration(self):
        if self.debug_level > 0:
            print "Calibrating..."
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0

        if self.debug_level > 0:        
            print "Turn sensor 360 slow..."

        for i in range(0,500):
            x = self.read_word_signed(X_OUTPUT_H)
            y = self.read_word_signed(Y_OUTPUT_H)
            z = self.read_word_signed(Z_OUTPUT_H)

            if x < x_min:
                x_min = x
    
            if y < y_min:
                y_min = y
    
            if x > x_max:
                x_max = x
    
            if y > y_max:
                y_max = y

            if self.debug_level > 0:
                print "%d  x = %d  y = %d" % (i,x,y)
            sleep(0.1)


        if self.debug_level > 0:
            print "min x = ", x_min, "  max x = ", x_max
            print "min y = ", y_min, "  max y = ", y_max

        self.x_offset = (x_max + x_min) / 2
        self.y_offset = (y_max + y_min) / 2

        if self.debug_level > 0:
            print "x offset =  ", self.x_offset
            print "y offset =  ", self.y_offset
            print "Done calibiration"

        # writing calibration data
        f = open(CALIB_FILE,'w')
        f.write(str(self.x_offset) + "\n")
        f.write(str(self.y_offset) + "\n")
        f.close()


    def get_bearing(self):
        scale = 0.92
        cx = (self.read_word_signed(X_OUTPUT_H) - self.x_offset) * scale
        cy = (self.read_word_signed(Y_OUTPUT_H) - self.y_offset) * scale
        cz = self.read_word_signed(Z_OUTPUT_H) * scale
        bearing  = math.atan2(cy,cx) 
        if (bearing < 0):
            bearing += 2 * math.pi
        return math.degrees(bearing)


    def read_word_signed(self,adr):
        rawData = self.bus.read_i2c_block_data(DEV_ADDR, adr, 2)
        return self.signed_int(rawData[0] << 8 | rawData[1])


    def signed_int(self,unsigned_int):
        if (unsigned_int >= 0x8000): # negative value                           
            return -((0xffff - unsigned_int) + 1)
        else:                        # positive value                           
            return unsigned_int
