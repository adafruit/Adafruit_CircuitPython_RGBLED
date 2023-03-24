# SPDX-FileCopyrightText: 2019 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# pylint: disable=raise-missing-from
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
    from typing import Union
except ImportError:
    pass

from pwmio import PWMOut

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_RGBLED.git"


class RGBLED:
    """
    Creates a RGBLED object given three physical pins or PWMOut objects.

    Example for setting a RGB LED using a RGB Tuple (Red, Green, Blue):

    .. code-block:: python

        import board
        import adafruit_rgbled

        RED_LED = board.D5
        GREEN_LED = board.D6
        BLUE_LED = board.D7

        # Create a RGB LED object
        led = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED)
        led.color = (255, 0, 0)

    Example for setting a RGB LED using a 24-bit integer (hex syntax):

    .. code-block:: python

        import board
        import adafruit_rgbled

        RED_LED = board.D5
        GREEN_LED = board.D6
        BLUE_LED = board.D7

        # Create a RGB LED object
        led = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED)
        led.color = 0x100000

    Example for setting a RGB LED using a ContextManager:

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
    """

    def __init__(
        self,
        red_pin: Union["microcontroller.Pin", PWMOut, "PWMChannel"],
        green_pin: Union["microcontroller.Pin", PWMOut, "PWMChannel"],
        blue_pin: Union["microcontroller.Pin", PWMOut, "PWMChannel"],
        invert_pwm: bool = False,
    ) -> None:
        """
        :param Union["microcontroller.Pin", PWMOut, "PWMChannel"] red_pin:
        The connection to the red LED.
        :param Union["microcontroller.Pin", PWMOut, "PWMChannel"] green_pin:
        The connection to the green LED.
        :param Union["microcontroller.Pin", PWMOut, "PWMChannel"] blue_pin:
        The connection to the blue LED.
        :param bool invert_pwm: False if the RGB LED is common cathode,
        True if the RGB LED is common anode. Defaults to False.
        """
        self._rgb_led_pins = [red_pin, green_pin, blue_pin]
        for pin, _ in enumerate(self._rgb_led_pins):
            try:
                pin_type = str(type(self._rgb_led_pins[pin]))
                if pin_type.startswith("<class '") and pin_type.endswith("Pin'>"):
                    self._rgb_led_pins[pin] = PWMOut(self._rgb_led_pins[pin])
                self._rgb_led_pins[pin].duty_cycle = 0
            except AttributeError:
                raise TypeError("Pins must be of type Pin, PWMOut or PWMChannel")
        self._invert_pwm = invert_pwm
        self._current_color = (0, 0, 0)
        self.color = self._current_color

    def __enter__(self) -> "RGBLED":
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.deinit()

    def deinit(self) -> None:
        """Turn the LEDs off, deinit pwmout and release hardware resources."""
        for pin in self._rgb_led_pins:
            pin.deinit()  # pylint: disable=no-member
        self._current_color = (0, 0, 0)

    @property
    def color(self) -> Union[int, tuple]:
        """
        Sets the RGB LED to a desired color.
        :param Union[int, tuple] value: RGB LED desired value - can be a RGB tuple of values
        0 - 255 or a 24-bit integer. e.g. (255, 64, 35) and 0xff4023 are equivalent.

        :raises ValueError: If the input is an int > 0xffffff or is a tuple that does not
          contain 3 integers of 0 - 255.
        :raises TypeError: If the input is not an integer or a tuple.
        """
        return self._current_color

    @color.setter
    def color(self, value: Union[int, tuple]):
        if isinstance(value, int):
            try:
                # Check that integer is <= 0xffffff and create an iterable.
                rgb = value.to_bytes(3, "big", signed=False)
            except OverflowError:
                raise ValueError("Only bits 0->23 valid for integer input")
        elif isinstance(value, tuple):
            try:
                rgb = bytes(value)  # Check that tuple has integers of 0 - 255.
                if len(rgb) != 3:
                    raise ValueError
            except (ValueError, TypeError):
                raise ValueError(
                    "Only a tuple of 3 integers of 0 - 255 for tuple input."
                )
        else:
            raise TypeError(
                "Color must be a tuple of 3 integers or 24-bit integer value."
            )
        for color, intensity in enumerate(rgb):
            # Take advantage of bool truthiness.
            self._rgb_led_pins[color].duty_cycle = abs(
                intensity * 257 - 65535 * self._invert_pwm
            )
        self._current_color = value
