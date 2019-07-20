from signal import pause
from time import time
from os import environ
from mpd import MPDClient
from mpd.base import ConnectionError
from rotary import RotaryEncoderClickable


class State(object):
    last = None
    direct = 1


state = State()


rotary = RotaryEncoderClickable(14, 15, 18)
mpd_host = environ.get("MPD_HOST", "localhost")

client = MPDClient()
client.timeout = 3

state.last = time()


def connect():
    client.connect(mpd_host, 6600)


def current_volume():
    return int(client.status()["volume"])


def change(value):
    now = time()
    diff = now - state.last


    if value > 0:
        if state.direct == -1 and diff < 0.150:
            print("Ignore clockwise", diff)
            return

        print("clockwise", value)
        try:
            client.setvol(current_volume() + 4)
        except ConnectionError:
            connect()
            return

        state.direct = 1
        state.last = now

    else:
        if state.direct == 1 and diff < 0.150:
            print("Ignore counter", diff)
            return

        print("counter", value)
        try:
            client.setvol(current_volume() - 5)
        except ConnectionError:
            connect()
            return

        state.direct = -1
        state.last = now


def clicked():
    print("Clicked")
    try:
        client.pause()
    except ConnectionError:
        connect()
        return


rotary.when_pressed = clicked
rotary.when_rotated = change


def main():
    connect()
    print(client.status())
    pause()


if __name__ == "__main__":
    main()
