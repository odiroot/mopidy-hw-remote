#!/usr/bin/env python
"""
Note: this one is only going to work with Python + luma.

Establish the available space for display text on SSD1306.
Test everything actually renders.
"""
import time

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

# Text as in SSD1306 with Framebuf on MicroPython.
DX = 8
# Framebuf text height + some breathing space.
DY = 8 + 1


def main():
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)

    with canvas(device) as draw:
        for i in range(0, 16):
            for j in range(0, 7):
                c = chr(65 + (i + j) % 26)

                draw.text(
                    (i * DX, j * DY),
                    c,
                    fill="white"
                )

    while True:
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

# Can use 6 lines of 15 characters (8x8 pixels) max. 
# One pixel distance between lines.
