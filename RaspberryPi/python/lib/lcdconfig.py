# /*****************************************************************************
# * | File        :	  epdconfig.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-06-21
# * | Info        :   
# ******************************************************************************
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import os
import sys
import time
import spidev
import logging
import numpy as np

# https://pypi.org/project/gpiod/
import gpiod
chip = gpiod.chip('gpiochip0')  
import Hobot.GPIO as GPIO

class RaspberryPi:
    def __init__(self,spi=spidev.SpiDev(1,0),spi_freq=12000000,rst = 28,dc = 29,bl = 18,bl_freq=1000,i2c=None,i2c_freq=100000):
        self.np=np
        self.INPUT = False
        self.OUTPUT = True

        self.SPEED  =spi_freq
        self.BL_freq=bl_freq

        self.RST_PIN= self.gpio_mode(rst,self.OUTPUT)
        # self.DC_PIN = self.gpio_mode(dc,self.OUTPUT)
        self.DC_PIN=dc
        self.BL_PIN = self.gpio_pwm(bl)
        self.bl_DutyCycle(0)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(22, GPIO.OUT)
        #Initialize SPI
        self.SPI = spi
        if self.SPI!=None :
            self.SPI.max_speed_hz = spi_freq
            self.SPI.mode = 0

    def gpio_mode(self,Pin,Mode,pull_up = None,active_state = True):
        print(Pin, Mode, pull_up, active_state)
        line = chip.get_line(Pin)
        try:
            import os
            os.system("echo %d > /sys/class/gpio/unexport" % Pin)
        except Exception as e:
            pass
        config = gpiod.line_request()
        config.consumer = "lcd"
        config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        # config.flags = line.LINE_FLAG_BIAS_PULL_UP if pull_up else 0
        line.request(config)
        return Pin
        # if Mode:
        #     return DigitalOutputDevice(Pin,active_high = True,initial_value =False)
        # else:
        #     return DigitalInputDevice(Pin,pull_up=pull_up,active_state=active_state)

    def digital_write(self, Pin, value):
        # print("digital_write", str(Pin), value)
        # GPIO.output(Pin, GPIO.HIGH if value else GPIO.LOW)
        if Pin == 29:
            # print(1)
            GPIO.output(22,GPIO.HIGH if value else GPIO.LOW)
        else:
            line = chip.get_line(Pin)
            line.set_value(1 if value else 0)

    def digital_read(self, Pin):
        return Pin.value

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def gpio_pwm(self, Pin):
        print(Pin)
        # return PWMOutputDevice(Pin,frequency = self.BL_freq)

    def spi_writebyte(self, data):
        if self.SPI!=None :
            self.SPI.writebytes(data)

    def bl_DutyCycle(self, duty):
        # self.BL_PIN.value = duty / 100
        pass
        
    def bl_Frequency(self,freq):# Hz
        self.BL_PIN.frequency = freq
           
    def module_init(self):
        if self.SPI!=None :
            self.SPI.max_speed_hz = self.SPEED        
            self.SPI.mode = 0b00
        return 0

    def module_exit(self):
        logging.debug("spi end")
        if self.SPI!=None :
            self.SPI.close()
        
        logging.debug("gpio cleanup...")
        self.digital_write(self.RST_PIN, 1)
        self.digital_write(self.DC_PIN, 1)   
        # self.BL_PIN.close()
        time.sleep(0.001)



'''
if os.path.exists('/sys/bus/platform/drivers/gpiomem-bcm2835'):
    implementation = RaspberryPi()

for func in [x for x in dir(implementation) if not x.startswith('_')]:
    setattr(sys.modules[__name__], func, getattr(implementation, func))
'''

### END OF FILE ###
