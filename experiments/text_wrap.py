#!/usr/bin/env python
"""
Note: this one is only going to work with Python + luma.

Render text that doesn't fit in one line.
Simulation of displaying artist name and track name.

Note: requires micropython-textwrap in production.
"""
import sys
import time
import textwrap

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

# Text as in SSD1306 with Framebuf on MicroPython.
DX = 8
# Framebuf text height + some breathing space.
DY = 8 + 1
# Text area on the screen.
TW = 15
TH = 6


serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)


def wrap(text):
    return textwrap.wrap(text, TW,
                         # Note: MicroPython's str has limitations.
                         expand_tabs=False, replace_whitespace=False)


def wrap_cut(text, max_lines=2):
    lines = wrap(text)

    # The whole text (even split) fits in X lines.
    if len(lines) <= max_lines:
        return lines

    # Doesn't fit. Cut extra lines & Add ellipsis.
    return [
        lines[0],
        lines[1][:TW-2] + "..."
    ]


def write_line(drawer, text, row=0):
    for ci, character in enumerate(text):
        drawer.text(
            (ci * DX, row * DY),
            character,
            fill="white"
        )


def main():
    assert len(sys.argv) > 2
    artist, title = sys.argv[1:3]

    text_lines = wrap_cut(artist) + wrap_cut(title)

    with canvas(device) as draw:
        # luma.render uses really skinny font.
        # Pretend to have the same font as Framebuf.
        for li, line in enumerate(text_lines):
            write_line(draw, line, li)

        # Fake status info.
        write_line(draw, "Playing     @25%", row=6)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
