import time
import board
import adafruit_rgbled

# color types
red_tuple = (100, 0, 0)
green_tuple = (0, 100, 0)
blue_tuple = (0, 0, 100)

# hex types
red_hex = 0x100000

# TODO: integer types

led = adafruit_rgbled.RGBLED(board.D5, board.D6, board.D7)
print('RGB LED Brightness: ', led.brightness)

color = led.color
print(color)


led.color = red_tuple
time.sleep(1)
led.color = green_tuple
time.sleep(1)
led.color = blue_tuple
time.sleep(1)
led.color = red_hex
time.sleep(1)