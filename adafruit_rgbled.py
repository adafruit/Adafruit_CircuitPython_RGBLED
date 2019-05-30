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
    def __init__(self, red_pin, green_pin, blue_pin, brightness=1.0, invert_pwm=False):
        """Initializes a RGB LED.
        :param int red_pin: Red Anode Pin.
        :param int green_pin: Green Anode Pin.
        :param int blue_pin: Blue Anode Pin.
        :param float brightness: Optional RGB LED brightness.
        :param bool invert_pwm: Use inverted PWM (Common anode).
        """
        self._red_led = pulseio.PWMOut(red_pin)
        self._green_led = pulseio.PWMOut(green_pin)
        self._blue_led = pulseio.PWMOut(blue_pin)
        self._rgb_led_pins = [self._red_led, self._green_led, self._blue_led]
        self._brightness = brightness
        self._invert_pwm = invert_pwm
        self._current_color = (0, 0, 0)
        self.color = self._current_color

    def deinit(self):
        """Turn the LEDs off, deinit pwmout and release hardware resources.
        """
        for pin in pins:
            pin.duty_cycle = 0
            pin.deinit()
        self._current_color = None

    @property
    def frequency(self):
        """Returns the frequency of the RGB LED.
        """
        return self.frequency
    
    @frequency.setter
    def frequency(self, frequency_val):
        """Sets the RGB LED's PWM frequency.
        :param int frequency: 32 bit frequency value, in Hz.
        """
        self.frequency = frequency_val

    @property
    def brightness(self):
        """Returns the brightness of the RGB LED.
        """
        return self._brightness
    
    @property
    def color(self):
        """Returns the RGB LED's current color.
        """
        return self._current_color

    def map_range(self, x, in_min, in_max, out_min, out_max):
        """
        Maps a number from one range to another.
        Note: This implementation handles values < in_min differently than arduino's map function does.
        :return: Returns value mapped to new range
        :rtype: float
        """
        mapped = (x-in_min) * (out_max - out_min) / (in_max-in_min) + out_min
        if out_min <= out_max:
            return max(min(mapped, out_max), out_min)
        return min(max(mapped, out_max), out_min)

    @color.setter
    def color(self, value):
        """Sets the RGB LED to a desired color.
        :param type value: RGB LED desired value - can be a tuple, 24-bit integer,

        """
        print('Setting to ', value)
        if isinstance(value, tuple):
            for i in range(0,3):
                color = self._set_duty_cycle(value[i])
                self._rgb_led_pins[i].duty_cycle=color
        elif isinstance(value, int):
            if value>>24:
                raise ValueError("only bits 0->23 valid for integer input")
            r = value >> 16
            print(r)
            g = (value >> 8) & 0xff
            b = value & 0xff
            print('RGB Val: ', r, g, b)
            r = int(self.map_range(r, 0, 255, 0, 65535))
            g = int(self.map_range(g, 0, 255, 0, 65535))
            b = int(self.map_range(b, 0, 255, 0, 65535))
            print('post map: ', r, g, b)
            if self._invert_pwm:
                r -= 65535
                g -= 65535
                b -= 65535
            print('Invert: ', r, g, b)
            self._rgb_led_pins[0].duty_cycle = abs(r)
            self._rgb_led_pins[1].duty_cycle = abs(g)
            self._rgb_led_pins[2].duty_cycle = abs(b)
        else:
            raise ValueError('Color must be a tuple or 24-bit integer value.')

    def _set_duty_cycle(self, percent):
        """Converts a provided percentage into a 16-bit integer duty_cycle.
        :param int percent: Percentage value, from 0% to 100%.
        """
        if self._invert_pwm:
            data = int(percent / 100.0 * 65535.0) - 65535
            if data < 0:
                data = abs(data)
            return data
        return int(percent / 100.0 * 65535.0)