# The MIT License (MIT)
#
# Copyright (c) 2019 Brent Rubell for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_rgbled`
================================================================================

CircuitPython driver for RGB LEDs


* Author(s): Brent Rubell

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""
import math
from board import *
import pulseio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGBLED.git"

class RGBLED:
    """
    RGB LED Driver Class.
    """
    def init(self, red_pin, green_pin, blue_pin, brightness=1.0):
        """Initializes a RGB LED.
        :param int red_pin: Red Anode Pin.
        :param int green_pin: Green Anode Pin.
        :param int blue_pin: Blue Anode Pin.
        """
        self._red_led = pulseio.PWMOut(red_pin, variable_frequency=True)
        self._green_led = pulseio.PWMOut(green_pin, variable_frequency=True)
        self._blue_led = pulseio.PWMOut(blue_pin, variable_frequency=True)
        self.brightness = brightness
    
    def deinit(self):
        """Turn the LEDs off, deinit pwmout and release hardware resources.
        """
        self._red_led.duty_cycle = 0
        self._green_led.duty_cycle = 0
        self._blue_led.duty_cycle = 0
        self._red_led.deinit()
        self._blue_led.deinit()
        self._green_led.deinit()