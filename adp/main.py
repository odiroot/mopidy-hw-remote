#!/usr/bin/env python3
import logging
import signal
import sys
from queue import Queue
from threading import Event, current_thread

from config import DEBUG, PIN_A_NUM, PIN_B_NUM, PIN_BUT_NUM, MPD_HOST
from hardware import RotaryEncoder  # Only on RPi :(
from mpdc import MopidyClient


logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
log = logging.getLogger(__name__)

# TODO: Extract constants.
ACT_PUSH = 0
ACT_DOWN = -1
ACT_UP = 1


def main():
    log.info('Starting MPD remote controller...')
    queue = Queue()
    event = Event()
    client = MopidyClient(hostname=MPD_HOST)

    # Runs in the main thread to handle the work assigned to us by the
    # callbacks.
    def consume_queue():
        # If we fall behind and have to process many queue entries at once,
        # we can catch up by only calling `amixer` once at the end.
        while not queue.empty():
            action = queue.get()
            t = current_thread()
            log.debug('Got action: %s, thread %s %s', action, t.name, t.ident)

            if action == ACT_PUSH:
                client.toggle()
            elif action == ACT_UP:
                client.volume_inc()
            elif action == ACT_DOWN:
                client.volume_dec()

    # on_turn and on_press run in the background thread. We want them to do
    # as little work as possible, so all they do is enqueue the volume delta.
    def on_turn(delta):
        queue.put(delta)
        event.set()

    def on_press(value):
        # We'll use a value of 0 to signal that the main thread should toggle
        # its mute state.
        queue.put(ACT_PUSH)
        event.set()

    # Clean up before hard exit.
    def on_exit(a, b):
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


if __name__ == '__main__':
    main()
