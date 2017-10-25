from os import environ
from signal import pause

import RPi.GPIO as GPIO
from mpd import MPDClient
from mpd.base import ConnectionError


leg_a = 15
leg_b = 14
mpd_host = environ.get("MPD_HOST", "localhost")

client = MPDClient()
client.timeout = 3


GPIO.setmode(GPIO.BCM)
GPIO.setup([leg_a, leg_b], GPIO.IN, pull_up_down=GPIO.PUD_UP)

previous = None


def connect():
    client.connect(mpd_host, 6600)


def current_volume():
    return int(client.status()["volume"])


def change_volume(direction):
    try:
        current = current_volume()
        if direction:
            new = current + 3
        else:
            new = current - 3

        new = max(new, 3)
        new = min(new, 95)

        if new != current:
            client.setvol(new)

        print('New volume: %d' % new)
    except ConnectionError:
        connect()


def on_rotate(channel):
    global previous

    # Software debounce, ignore direction skips.
    if channel == previous:
        return
    else:
        previous = channel

    # Reduce number of triggers, only on B leading.
    if channel == leg_a:
        return  # A only used for debouncing.

    sig_a = GPIO.input(leg_a)
    sig_b = GPIO.input(leg_b)

    ones = sig_a + sig_b + 1
    if ones == 1 or ones == 3:
        # Backwards
        change_volume(0)
    elif ones == 0 or ones == 2:
        # Forward
        change_volume(1)


def main():
    connect()
    print(client.status())

    GPIO.add_event_detect(leg_a, GPIO.BOTH, callback=on_rotate)
    GPIO.add_event_detect(leg_b, GPIO.BOTH, callback=on_rotate)

    try:
        pause()
    except Exception:
        print('Quitting...')
    finally:
        GPIO.cleanup([leg_a, leg_b])


if __name__ == "__main__":
    main()
