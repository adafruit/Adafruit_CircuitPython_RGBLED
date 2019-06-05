import time
import board
import busio
from digitalio import DigitalInOut
import adafruit_rgbled
from adafruit_esp32spi import adafruit_esp32spi

# If you have an externally connected ESP32:
esp32_cs = DigitalInOut(board.D13)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

RED_LED = 26
GREEN_LED = 25
BLUE_LED = 27

# Create the RGB LED Object
led = adafruit_rgbled.RGBLED(RED_LED, GREEN_LED, BLUE_LED, esp)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return int(255 - pos * 3), int(pos * 3), 0
    if pos < 170:
        pos -= 85
        return 0, int(255 - pos * 3), int(pos * 3)
    pos -= 170
    return int(pos * 3), 0, int(255 - (pos * 3))

def rainbow_cycle(wait):
    for i in range(255):
        i = (i + 1) % 256
        led.color = wheel(i)
        time.sleep(wait)

while True:
    # setting RGB LED color to RGB Tuples (R, G, B)
    print('setting color 1')
    led.color = (255, 0, 0)
    time.sleep(1)

    print('setting color 2')
    led.color = (0, 255, 0)
    time.sleep(1)

    print('setting color 3')
    led.color = (0, 0, 255)
    time.sleep(1)

    # setting RGB LED color to 24-bit integer values
    led.color = 0xFF0000
    time.sleep(1)

    led.color = 0x00FF00
    time.sleep(1)

    led.color = 0x0000FF
    time.sleep(1)

    # rainbow cycle the RGB LED
    rainbow_cycle(0.1)
