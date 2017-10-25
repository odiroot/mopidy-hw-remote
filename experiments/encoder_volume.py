#!/usr/bin/env python
from signal import pause
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

leg_a = 15
leg_b = 14

GPIO.setup([leg_a, leg_b], GPIO.IN, pull_up_down=GPIO.PUD_UP)

previous = None
volume = 0


def change_volume(direction):
    global volume

    volume += 3 * direction
    volume = min(volume, 100)
    volume = max(volume, 0)

    print "Current volume: %d%%" % volume


def on_rotate(channel):
    global previous
    global volume

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
        change_volume(-1)
    elif ones == 0 or ones == 2:
        # Forward
        change_volume(1)


GPIO.add_event_detect(leg_a, GPIO.BOTH, callback=on_rotate)
GPIO.add_event_detect(leg_b, GPIO.BOTH, callback=on_rotate)


try:
    pause()
except Exception, e:
    pass
finally:
    GPIO.cleanup([leg_a, leg_b])
