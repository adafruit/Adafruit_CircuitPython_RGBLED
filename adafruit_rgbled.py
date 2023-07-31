# SPDX-FileCopyrightText: 2019 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

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
try:
    from typing import Union, Optional, Type
    from types import TracebackType
    from microcontroller import Pin
    from adafruit_pca9685 import PWMChannel
    from circuitpython_typing.led import ColorBasedColorUnion
except ImportError:
    pass

from pwmio import PWMOut

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGBLED.git"


class RGBLED:
    """
    Create an RGBLED object given three physical pins or PWMOut objects.

    Example for setting an RGB LED using an RGB Tuple (Red, Green, Blue):

    .. code-block:: python

        import board
        import adafruit_rgbled

        RED_LED = board.D5
        GREEN_LED = board.D6
        BLUE_LED = board.D7

        # Create a RGB LED object
        led = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED)
        led.color = (255, 0, 0)

    Example for setting an RGB LED using a 24-bit integer (hex syntax):

    .. code-block:: python

        import board
        import adafruit_rgbled

        RED_LED = board.D5
        GREEN_LED = board.D6
        BLUE_LED = board.D7

        # Create an RGB LED object
        led = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED)
        led.color = 0x100000

    Example for setting an RGB LED using a ContextManager:

    .. code-block:: python

        import board
        import adafruit_rgbled
        with adafruit_rgbled.RGBLED(board.D5, board.D6, board.D7) as rgb_led:
            rgb_led.color = (255, 0, 0)

    Example for setting a common-anode RGB LED using a ContextManager:

    .. code-block:: python

        import board
        import adafruit_rgbled
        with adafruit_rgbled.RGBLED(board.D5, board.D6, board.D7, invert_pwm=True) as rgb_led:
            rgb_led.color = (0, 255, 0)

    :param Union[Pin, PWMOut, "PWMChannel"] red_pin:
        The connection to the red LED.
    :param Union[Pin, PWMOut, "PWMChannel"] green_pin:
        The connection to the green LED.
    :param Union[Pin, PWMOut, "PWMChannel"] blue_pin:
        The connection to the blue LED.
    :param bool invert_pwm: False if the RGB LED is common cathode,
        True if the RGB LED is common anode. Defaults to False.
    """

    def __init__(
        self,
        red_pin: Union[Pin, PWMOut, PWMChannel],
        green_pin: Union[Pin, PWMOut, PWMChannel],
        blue_pin: Union[Pin, PWMOut, PWMChannel],
        invert_pwm: bool = False,
    ) -> None:
        self._rgb_led_pins = [red_pin, green_pin, blue_pin]
        for i in range(  # pylint: disable=consider-using-enumerate
            len(self._rgb_led_pins)
        ):
            if hasattr(self._rgb_led_pins[i], "frequency"):
                self._rgb_led_pins[i].duty_cycle = 0
            elif str(type(self._rgb_led_pins[i])) == "<class 'Pin'>":
                self._rgb_led_pins[i] = PWMOut(self._rgb_led_pins[i])
                self._rgb_led_pins[i].duty_cycle = 0
            else:
                raise TypeError("Must provide a pin, PWMOut, or PWMChannel.")
        self._invert_pwm = invert_pwm
        self._current_color = (0, 0, 0)
        self.color = self._current_color

    def __enter__(self) -> "RGBLED":
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[type]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.deinit()

    def deinit(self) -> None:
        """Turn the LEDs off, deinit pwmout and release hardware resources."""
        for pin in self._rgb_led_pins:
            pin.deinit()  # pylint: disable=no-member
        self._current_color = (0, 0, 0)

    @property
    def color(self) -> ColorBasedColorUnion:
        """
        Sets the RGB LED to a desired color.

        :param ColorBasedColorUnion value: RGB LED desired value - can be a RGB
            tuple of values 0 - 255 or a 24-bit integer. e.g. (255, 64, 35) and 0xff4023
            are equivalent.

        :returns Union[int, Tuple[int, int, int]]: The current LED color setting.

        :raises ValueError: If the input is an int > 0xffffff.
        :raises TypeError: If the input is not an integer or a tuple.
        """
        return self._current_color

    @color.setter
    def color(self, value: ColorBasedColorUnion):
        self._current_color = value
        if isinstance(value, tuple):
            for i in range(0, 3):
                color = int(max(0, min(65535, value[i] * 257)))
                if self._invert_pwm:
                    color -= 65535
                self._rgb_led_pins[i].duty_cycle = abs(color)
        elif isinstance(value, int):
            if value > 0xFFFFFF:
                raise ValueError("Only bits 0->23 valid for integer input")
            r = value >> 16
            g = (value >> 8) & 0xFF
            b = value & 0xFF
            rgb = [r, g, b]
            for color in range(0, 3):
                rgb[color] = max(0, min(65535, rgb[color] * 257))
                if self._invert_pwm:
                    rgb[color] -= 65535
                self._rgb_led_pins[color].duty_cycle = abs(rgb[color])
        else:
            raise TypeError("Color must be a tuple or 24-bit integer value.")
