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

* Adafruit's SimpleIO library: https://github.com/adafruit/Adafruit_CircuitPython_SimpleIO
"""
from pulseio import PWMOut
from simpleio import map_range

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGBLED.git"

class RGBLED:
    """
    RGB LED Driver Class.
    """
    def __init__(self, red_pin, green_pin, blue_pin, invert_pwm=False):
        """Initializes a RGB LED.
        :param int red_pin: Red Anode Pin.
        :param int green_pin: Green Anode Pin.
        :param int blue_pin: Blue Anode Pin.
        :param bool invert_pwm: Use inverted PWM (Common anode).
        """
        self._red_led = PWMOut(red_pin)
        self._green_led = PWMOut(green_pin)
        self._blue_led = PWMOut(blue_pin)
        self._rgb_led_pins = [self._red_led, self._green_led, self._blue_led]
        self._invert_pwm = invert_pwm
        self._current_color = (0, 0, 0)
        self.color = self._current_color

    def deinit(self):
        """Turn the LEDs off, deinit pwmout and release hardware resources."""
        for pin in self._rgb_led_pins:
            pin.deinit()

    @property
    def color(self):
        """Returns the RGB LED's current color."""
        return self._current_color

    @color.setter
    def color(self, value):
        """Sets the RGB LED to a desired color.
        :param type value: RGB LED desired value - can be a tuple, 24-bit integer,
        """
        if isinstance(value, tuple):
            for i in range(0, 3):
                color = self._set_duty_cycle(value[i])
                self._rgb_led_pins[i].duty_cycle = color
        elif isinstance(value, int):
            if value>>24:
                raise ValueError("Only bits 0->23 valid for integer input")
            r = value >> 16
            g = (value >> 8) & 0xff
            b = value & 0xff
            rgb = [r, g, b]
            for color in range(0, 3):
                rgb[color] = int(map_range(rgb[color], 0, 255, 0, 65535))
                if self._invert_pwm:
                    rgb[color] -= 65535
                self._rgb_led_pins[color].duty_cycle = abs(rgb[color])
        else:
            raise ValueError('Color must be a tuple or 24-bit integer value.')

    def _set_duty_cycle(self, percent):
        """Converts a percentage into a 16-bit duty_cycle integer value.
        :param int percent: Percentage value, from 0% to 100%.
        """
        if self._invert_pwm:
            data = int(percent / 100.0 * 65535.0) - 65535
            return abs(data)
        return int(percent / 100.0 * 65535.0)
