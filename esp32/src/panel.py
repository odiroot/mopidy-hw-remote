from machine import Pin
from abutton import Pushbutton


PIN_RED = const(13)
PIN_ORANGE = const(12)
PIN_GREEN = const(14)
PIN_YELLOW = const(27)


def __btn(num):
    return Pushbutton(
        pin=Pin(num, Pin.IN, Pin.PULL_UP),
        # Don't call release handler after long press.
        suppress=True
    )


class Panel:
    def __init__(self):
        self.red = __btn(PIN_RED)
        self.orange = __btn(PIN_ORANGE)
        self.green = __btn(PIN_GREEN)
        self.yellow = __btn(PIN_YELLOW)
