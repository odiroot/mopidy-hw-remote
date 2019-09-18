#!/usr/bin/env python3
import logging
import signal
import sys
from enum import Enum
from queue import Queue
from textwrap import fill
from threading import Event


from .config import (DEBUG, DISPLAY_TIMEOUT, FONT_NAME, FONT_SIZE, I2C_ADDRESS,
                     I2C_PORT, MQTT_HOST, MQTT_TOPIC, PIN_A_NUM, PIN_B_NUM,
                     PIN_BUT_NUM, VOLUME_STEP)
from .control import RotaryEncoder
from .display import Display
from .mqtt import MopidyClient


logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
log = logging.getLogger(__name__)


class EncoderActions(Enum):
    """Available rotary encoder actions to pass between threads."""
    PUSH = 0
    DOWN = -1
    UP = 1


def main():
    log.info('Starting MPD remote controller...')
    queue = Queue()
    event = Event()
    display = Display(
        address=I2C_ADDRESS, port=I2C_PORT,
        font_name=FONT_NAME, font_size=FONT_SIZE, timeout=DISPLAY_TIMEOUT)
    display.start()

    # XXX: Dirty.
    # Reacting to MQTT messages.
    def on_mqtt_msg(topic, payload):
        if topic == 'sta':
            return display.text('Playback:\n{}'.format(payload))
        if topic == 'vol':
            return display.text('Volume:\n{}'.format(payload))
        if topic == 'trk':
            title, artist, _ = payload.split(';')
            title = fill('* ' + title, 15)
            artist = fill('@ ' + artist, 15)
            return display.text('{}\n{}'.format(title, artist))

    client = MopidyClient(
        host=MQTT_HOST, topic=MQTT_TOPIC, callback=on_mqtt_msg)
    client.start()

    # Runs in the main thread to handle the work assigned to us by the
    # callbacks.
    def consume_queue():
        # If we fall behind and have to process many queue entries at once,
        # we can catch up by only calling `amixer` once at the end.
        while not queue.empty():
            action = queue.get()
            log.debug('Got action: %s', action)

            if action == EncoderActions.PUSH:
                client.toggle()
            elif action == EncoderActions.UP:
                client.volume_inc(VOLUME_STEP)
            elif action == EncoderActions.DOWN:
                client.volume_dec(VOLUME_STEP)

    # on_turn and on_press run in the background thread. We want them to do
    # as little work as possible, so all they do is enqueue the volume delta.
    def on_turn(delta):
        if delta > 0:
            queue.put(EncoderActions.UP)
        else:
            queue.put(EncoderActions.DOWN)
        event.set()

    def on_press(value):
        # We'll use a value of 0 to signal that the main thread should toggle
        # its mute state.
        queue.put(EncoderActions.PUSH)
        event.set()

    # Clean up before hard exit.
    def on_exit(a, b):
        client.stop()
        display.stop()

        log.info('Stopping MPD remote controller...')
        encoder.destroy()
        sys.exit(0)

    encoder = RotaryEncoder(
        gpio_a=PIN_A_NUM,
        gpio_b=PIN_B_NUM,
        gpio_button=PIN_BUT_NUM,
        callback=on_turn,
        button_callback=on_press
    )

    # Register cleanup handler.
    signal.signal(signal.SIGINT, on_exit)

    while True:
        # This is the best way I could come up with to ensure that this
        # script runs indefinitely without wasting CPU by polling. The main
        # thread will block quietly while waiting for the event to get
        # flagged. When the knob is turned we 're able to respond immediately,
        # but when it's not being turned we're not looping at all.
        #
        # The 1200-second (20 minute) timeout is a hack. For some reason, if
        # I don't specify a timeout, I'm unable to get the SIGINT handler
        # above to work properly. But if there is a timeout set, even if it's
        # a very long timeout, then Ctrl-C works as intended. No idea why.
        event.wait(1200)

        # If we're here because a callback told us to wake up, we should
        # consume whatever messages are in the queue. If we're here because
        # there were 20 minutes of inactivity, no problem; we'll just consume
        # an empty queue and go right back to sleep.
        consume_queue()
        event.clear()
