from machine import Pin

import uasyncio as asyncio
from abutton import Pushbutton


LED_PIN = const(25)
BTN_PIN = const(0)


button = Pushbutton(Pin(BTN_PIN, Pin.IN, Pin.PULL_UP))


async def _heartbeat():
    led = Pin(LED_PIN, Pin.OUT, value=0)

    while True:
        led(1)
        await asyncio.sleep_ms(200)
        led(0)
        await asyncio.sleep_ms(3000)


def enable_heartbeat():
    # Shost press the board button to start LED heartbeat.
    button.press_func(_heartbeat)


async def _stopper():
    print('Tripping the loop')
    raise StopIteration


def enable_stopper():
    # Long press the board button to stop the asyncio loop
    button.long_func(_stopper)
