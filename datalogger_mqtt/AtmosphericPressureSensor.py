#!/usr/bin/env python
# -*- coding:utf-8 -*-

#
#
# 大気圧の記録デーモン
#
# 2015/5/3 Maho Takara
#
#
import sys
import os
import smbus

DEVICE_ADDRESS = 0x5c
DEVICE_REG = 0x0F
bus = None

def init():

    global bus
    # 大気圧センサーの初期化
    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
    bus = smbus.SMBus(1)   

    # Read WHO_I_AM Reg
    buf = bus.read_byte_data(DEVICE_ADDRESS, DEVICE_REG)

    # Write CTRL_REG1  PWR=ON, OUTPUT 1Hz
    bus.write_byte_data(DEVICE_ADDRESS, 0x20, 0x90)


def get():
    pmb = 0
    try:
        # Read Atmospheric Pressure
        h_byte = bus.read_byte_data(DEVICE_ADDRESS, 0x2A)
        l_byte = bus.read_byte_data(DEVICE_ADDRESS, 0x29)
        xl_byte = bus.read_byte_data(DEVICE_ADDRESS, 0x28)
        pmb = (h_byte << 16 | l_byte << 8 | xl_byte) / 4096
    except:
        print "Unexpected error:", sys.exc_info()[0]

    return (0, {"pressure" : pmb})

###

