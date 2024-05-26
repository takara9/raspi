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
from smbus2 import SMBus 
from time   import sleep


# I2C
# slave address
DEV_ADDR   = 0x53

# register address
DEVID               = 0x00    # Device ID
THRESH_TAP          = 0x1D    # Tap threshold
OFSX                = 0x1E    # X-axis offset
OFSY                = 0x1F    # Y-axis offset
OFSZ                = 0x20    # Z-axis offset
DUR                 = 0x21    # Tap duration
LATENT              = 0x22    # Tap latency
WINDOW              = 0x23    # Tap window
THRESH_ACT          = 0x24    # Activity threshold
THRESH_INACT        = 0x25    # Inactivity threshold
TIME_INACT          = 0x26    # Inactivity time
ACT_INACT_CTL       = 0x27    # Axis enable control for activity and inactivity detection
THRESH_FF           = 0x28    # Free-fall threshold
TIME_FF             = 0x29    # Free-fall time
TAP_AXES            = 0x2A    # Axis control for single/double tap
ACT_TAP_STATUS      = 0x2B    # Source for single/double tap
BW_RATE             = 0x2C    # Data rate and power mode control
POWER_CTL           = 0x2D    # Power-saving features control
INT_ENABLE          = 0x2E    # Interrupt enable control
INT_MAP             = 0x2F    # Interrupt mapping control
INT_SOURCE          = 0x30    # Source of interrupts
DATA_FORMAT         = 0x31    # Data format control
DATAX0              = 0x32    # X-axis data 0
DATAX1              = 0x33    # X-axis data 1
DATAY0              = 0x34    # Y-axis data 0
DATAY1              = 0x35    # Y-axis data 1
DATAZ0              = 0x36    # Z-axis data 0
DATAZ1              = 0x37    # Z-axis data 1
FIFO_CTL            = 0x38    # FIFO control
FIFO_STATUS         = 0x39    # FIFO status

class adxl345:
    def __init__(self,debug):
	self.bus = SMBus(1)
        self.bus.write_byte_data(DEV_ADDR, BW_RATE,     0x0A) # 100Hz
        self.bus.write_byte_data(DEV_ADDR, DATA_FORMAT, 0x00) # 10bit 2g
        self.bus.write_byte_data(DEV_ADDR, FIFO_CTL,    0x00) # FIFO_CTL  OFF
        self.bus.write_byte_data(DEV_ADDR, POWER_CTL,   0x08) # POWER_CTL ON
        self.bus.write_byte_data(DEV_ADDR, OFSX, 0x0)
        self.bus.write_byte_data(DEV_ADDR, OFSY, 0x0)
        self.bus.write_byte_data(DEV_ADDR, OFSZ, 0x0)
        self.debug_level = debug

    def signed_int(self,unsigned_int):
        if (unsigned_int >= 0x8000): # negative value
            return -((0xffff - unsigned_int) + 1)
        else:                        # positive value
            return unsigned_int


    def selfTest(self):
        self.bus.write_byte_data(DEV_ADDR, BW_RATE,     0x0A) # 100Hz
        self.bus.write_byte_data(DEV_ADDR, DATA_FORMAT, 0x03) # 16g test-mode = off, FULL_RES = 0
        
        n_sample = 10
        x_st_off_sum = 0
        y_st_off_sum = 0
        z_st_off_sum = 0

        for i in range(0,n_sample):
            data = self.bus.read_i2c_block_data(DEV_ADDR, DATAX0, 6)
            if self.debug_level > 1:
                print i, "Xoff=",self.signed_int(data[1] << 8 | data[0])
                print i, "Yoff=",self.signed_int(data[3] << 8 | data[2])
                print i, "Zoff=",self.signed_int(data[5] << 8 | data[4])
            x_st_off_sum += self.signed_int(data[1] << 8 | data[0])
            y_st_off_sum += self.signed_int(data[3] << 8 | data[2])
            z_st_off_sum += self.signed_int(data[5] << 8 | data[4])
            sleep(0.02)

        # Sampling data in normal mode
        x_st_off = x_st_off_sum / n_sample
        y_st_off = y_st_off_sum / n_sample
        z_st_off = z_st_off_sum / n_sample

        self.bus.write_byte_data(DEV_ADDR, DATA_FORMAT, 0x83) # 16g test-mode = on

        # Wait until to be stable during 4 samples
        for i in range(0,12):
            data = self.bus.read_i2c_block_data(DEV_ADDR, DATAX0, 6)

        # 
        x_st_on_sum = 0
        y_st_on_sum = 0
        z_st_on_sum = 0

        for i in range(0,n_sample):
            data = self.bus.read_i2c_block_data(DEV_ADDR, DATAX0, 6)
            if self.debug_level > 1:
                print i, "Xon=",self.signed_int(data[1] << 8 | data[0])
                print i, "Yon=",self.signed_int(data[3] << 8 | data[2])
                print i, "Zon=",self.signed_int(data[5] << 8 | data[4])
            x_st_on_sum += self.signed_int(data[1] << 8 | data[0])
            y_st_on_sum += self.signed_int(data[3] << 8 | data[2])
            z_st_on_sum += self.signed_int(data[5] << 8 | data[4])
            sleep(0.02)

        # Sampling data in test mode
        x_st_on = x_st_on_sum / n_sample
        y_st_on = y_st_on_sum / n_sample
        z_st_on = z_st_on_sum / n_sample

        x_st = (x_st_on - x_st_off) * 1.77 # 3.3v X-Axis scale
        y_st = (y_st_on - y_st_off) * 1.77 # 3.3v Y-Axis scale
        z_st = (z_st_on - z_st_off) * 1.47 # 3.3v Z-Axis scale
        
        if self.debug_level > 0:
            print "X = %3.1f LSB" % x_st
            print "Y = %3.1f LSB" % y_st
            print "Z = %3.1f LSB" % z_st

        test_ng = 0
        if self.debug_level > 0:
            print "SELF TEST X-Axis :",

        if x_st > 6 and x_st < 67:
            if self.debug_level > 0:
                print "OK"
        else:
            if self.debug_level > 0:
                print "NG"
            test_ng += 1

        if self.debug_level > 0:
            print "SELF TEST Y-Axis :",

        if y_st > -67 and y_st < -6:
            if self.debug_level > 0:
                print "OK"
        else:
            if self.debug_level > 0:
                print "NG"
            test_ng += 1

        if self.debug_level > 0:
            print "SELF TEST Z-Axis :",
        if z_st > 10 and z_st < 110:
            if self.debug_level > 0:
                print "OK"
        else:
            if self.debug_level > 0:
                print "NG"
            test_ng += 1

        # reset self test mode
        self.bus.write_byte_data(DEV_ADDR, DATA_FORMAT, 0x03) # 16g test-mode = off
        return test_ng
        
    def calibration(self):        
        self.bus.write_byte_data(DEV_ADDR, BW_RATE,     0x0A) # 100Hz
        self.bus.write_byte_data(DEV_ADDR, DATA_FORMAT, 0x00) # 2g
        sleep(0.01)

        n_sample = 10
        x_sum = 0
        y_sum = 0
        z_sum = 0

        for i in range(0,n_sample):
            data = self.bus.read_i2c_block_data(DEV_ADDR, DATAX0, 6)
            if self.debug_level > 1:
                print i,"X_0g =",self.signed_int(data[1] << 8 | data[0])
                print i,"Y_0g =",self.signed_int(data[3] << 8 | data[2])
                print i,"Z_1g =",self.signed_int(data[5] << 8 | data[4])
            x_sum += self.signed_int(data[1] << 8 | data[0])
            y_sum += self.signed_int(data[3] << 8 | data[2])
            z_sum += self.signed_int(data[5] << 8 | data[4])
            sleep(0.02)

        # Sampling data in normal mode
        x0 = x_sum / n_sample
        y0 = y_sum / n_sample
        z1 = z_sum / n_sample
        # Typ ±2g,10-bit resolution = 256 LSB/g
        z0 = z1 - 256

        if self.debug_level > 0:
            print "X_0g average = %2.1f LSB" % x0
            print "Y_0g average = %2.1f LSB" % y0
            print "Z_0g average = %2.1f LSB" % z0

        x_offset = int(-round(x0/4))
        y_offset = int(-round(y0/4))
        z_offset = int(-round(z0/4))

        if self.debug_level > 0:
            print "X_offset = %2.1f LSB" % x_offset
            print "Y_offset = %2.1f LSB" % y_offset
            print "Z_offset = %2.1f LSB" % z_offset

        self.bus.write_byte_data(DEV_ADDR, OFSX, x_offset)
        self.bus.write_byte_data(DEV_ADDR, OFSY, y_offset)
        self.bus.write_byte_data(DEV_ADDR, OFSZ, z_offset)

        
    def get_accel(self):
        self.bus.write_byte_data(DEV_ADDR, BW_RATE,     0x0A) # 100Hz
        self.bus.write_byte_data(DEV_ADDR, DATA_FORMAT, 0x00) # 2g
        #self.bus.write_byte_data(DEV_ADDR, DATA_FORMAT, 0x02) #  8g
        sleep(0.01)
        
        n_sample = 10
        x_sum = 0
        y_sum = 0
        z_sum = 0

        for i in range(0,n_sample):
            data = self.bus.read_i2c_block_data(DEV_ADDR, DATAX0, 6)

            if self.debug_level > 1:
                print i,"X_0g =",self.signed_int(data[1] << 8 | data[0])
                print i,"Y_0g =",self.signed_int(data[3] << 8 | data[2])
                print i,"Z_1g =",self.signed_int(data[5] << 8 | data[4])
            x_sum += self.signed_int(data[1] << 8 | data[0])
            y_sum += self.signed_int(data[3] << 8 | data[2])
            z_sum += self.signed_int(data[5] << 8 | data[4])
            sleep(0.02)

        x = (x_sum / n_sample) * 3.9
        y = (y_sum / n_sample) * 3.9
        z = (z_sum / n_sample) * 3.9
        
        return(x,y,z)
        
