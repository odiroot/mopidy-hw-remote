from micropython import const
from machine import Pin
from abutton import Pushbutton


PIN_ANTENNA = const(14)
PIN_SOCKET = const(12)


def __btn(num):
    return Pushbutton(
        pin=Pin(num, Pin.IN, Pin.PULL_UP),
        # Don't call release handler after long press.
        suppress=True
    )


class Panel:
    def __init__(self, client):
        self.client = client

        # Initialise async handling of buttons.
        self.antenna = __btn(PIN_ANTENNA)
        self.socket = __btn(PIN_SOCKET)

        # Bind the button input to controller handlers.
        self.antenna.release_func(self.on_antenna_short)
        self.socket.release_func(self.on_socket_short)
        self.antenna.long_func(self.on_antenna_long)
        self.socket.long_func(self.on_socket_long)

    async def on_antenna_short(self):
        print("Volume up")
        await self.client.send('mopidy/c/vol', '+5')

    async def on_socket_short(self):
        print("Volume down")
        await self.client.send('mopidy/c/vol', '-5')

    async def on_antenna_long(self):
        print("Speakers toggle")
        await self.client.send('cmnd/speakers/power', 'toggle')

    async def on_socket_long(self):
        print("Playback toggle")
        await self.client.send('mopidy/c/plb', 'toggle')
