#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

def init_gpio(pin):
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        return 0
    except OSError as err:
        print("OS error:", err)
    except ValueError as err:
        print("GPIO Error: ", err)
        return 1
    except Exception as err:
        print("Unexpected error: ", err)
        return 1
    

def power_sw(pin,keep):
    try:
        GPIO.output(pin, True)
        time.sleep(float(keep/1000))
        GPIO.output(pin, False)
        return 'ok'
    except OSError as err:
        print("OS error: ", err)
        return err
    except ValueError as err:
        print("GPIO Error: ", err)
        return err
    except Exception as err:
        print("Unexpected error: ", err)
        return err



def power_on(pin):
    try:
        GPIO.output(pin, True)
        return 'ok'
    except OSError as err:
        print("OS error: ", err)
        return err
    except ValueError as err:
        print("GPIO Error: ", err)
        return err
    except Exception as err:
        print("Unexpected error: ", err)
        return err


def power_off(pin):
    try:
        GPIO.output(pin, False)
        return 'ok'
    except OSError as err:
        print("OS error: ", err)
        return err
    except ValueError as err:
        print("GPIO Error: ", err)
        return err
    except Exception as err:
        print("Unexpected error: ", err)
        return err
    

