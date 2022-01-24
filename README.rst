CircuitPython_RGBLED
====================
.. image:: https://readthedocs.org/projects/adafruit-circuitpython-rgbled/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/rgbled/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_RGBLED/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_RGBLED/actions
    :alt: Build Status

CircuitPython driver for RGB LEDs. Works with native microcontroller pins,
`Adafruit Blinka <https://github.com/adafruit/Adafruit_Blinka>`_, or the `PCA9685 PWM driver <https://www.adafruit.com/product/815>`_.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `SimpleIO Library <https://github.com/adafruit/Adafruit_CircuitPython_SimpleIO>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
--------------------
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-rgbled/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-rgbled

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-rgbled

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-rgbled

Usage Example
==============

Initialize a common-cathode RGB LED with three PWM-capable pins.

.. code-block:: python

    import board
    import adafruit_rgbled

    # Pin the Red LED is connected to
    RED_LED = board.D5

    # Pin the Green LED is connected to
    GREEN_LED = board.D6

    # Pin the Blue LED is connected to
    BLUE_LED = board.D7

    # Create a RGB LED object
    led = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED)

Initialize a common-anode RGB LED with three PWM-capable pins

.. code-block:: python

    import board
    import adafruit_rgbled

    # Pin the Red LED is connected to
    RED_LED = board.D5

    # Pin the Green LED is connected to
    GREEN_LED = board.D6

    # Pin the Blue LED is connected to
    BLUE_LED = board.D7

    # Create a RGB LED object
    led = adafruit_rgbled.RGBLED(RED_LED, BLUE_LED, GREEN_LED, invert_pwm = True)

Set the RGB LED's color to a RGB Tuple (Red, Green, Blue).

.. code-block:: python

    led.color = (255, 0, 0)

Set the RGB LED's color to a 24-bit integer (in hex syntax), 0x100000.

.. code-block:: python

    led.color = 0x100000

Setting a common-anode RGB LED using a ContextManager:

.. code-block:: python

    import board
    import adafruit_rgbled
    with adafruit_rgbled.RGBLED(board.D5, board.D6, board.D7, invert_pwm = True) as rgb_led:
        rgb_led.color = (0, 255, 0)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/rgbled/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_RGBLED/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
