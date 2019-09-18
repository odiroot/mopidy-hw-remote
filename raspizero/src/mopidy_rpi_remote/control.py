"""
Source: https://andrewdupont.net/2017/04/28/
        nostalgia-tron-part-6-adding-a-volume-knob-to-the-raspberry-pi/
"""
from RPi import GPIO


class RotaryEncoder():
    """
    A class to decode mechanical rotary encoder pulses.

    Ported to RPi.GPIO from the pigpio sample here:
    http://abyz.me.uk/rpi/pigpio/examples.html
    """

    def __init__(self, gpio_a, gpio_b, callback=None, gpio_button=None,
                 button_callback=None):
        self.last_gpio = None
        self.gpio_a = gpio_a  # Encoder pin A.
        self.gpio_b = gpio_b  # Encoder pin B.
        self.gpio_button = gpio_button  # Push button on encoder.

        self.callback = callback
        self.button_callback = button_callback

        self.lev_a = 0
        self.lev_b = 0

        GPIO.setmode(GPIO.BCM)
        # Both encoder inputs pulled up (reacting to 0 signal).
        GPIO.setup(self.gpio_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.gpio_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Listen to both rising and falling edges.
        GPIO.add_event_detect(self.gpio_a, GPIO.BOTH, self._callback)
        GPIO.add_event_detect(self.gpio_b, GPIO.BOTH, self._callback)

        if self.gpio_button:
            GPIO.setup(self.gpio_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            # Push button pressed on 1->0 change.
            # Debouncing for 0.5s to ignore duplicate events.
            GPIO.add_event_detect(self.gpio_button, GPIO.FALLING,
                                  self._button_callback, bouncetime=500)

    def destroy(self):
        try:  # Easily fails on emulator, silence.
            GPIO.remove_event_detect(self.gpio_a)
            GPIO.remove_event_detect(self.gpio_b)
        except Exception:
            pass
        GPIO.cleanup((self.gpio_a, self.gpio_b, self.gpio_button))

    def _button_callback(self, channel):
        self.button_callback(GPIO.input(channel))

    def _callback(self, channel):
        level = GPIO.input(channel)
        # Remember last input from currently triggered pin.
        if channel == self.gpio_a:
            self.lev_a = level
        else:
            self.lev_b = level

        # Caught in the middle of a jump, just ignore until both phases pass.
        if level != 1:
            return

        # When both inputs are at 1, we'll fire a callback. If A was the most
        # recent pin set high, it'll be forward, and if B was the most recent
        # pin set high, it'll be reverse.
        if channel != self.last_gpio:  # (debounce)
            # Remember last triggered pin. In perfect world they should always
            # alternate. This is why we ignore repeated triggers (above ^).
            self.last_gpio = channel
            if channel == self.gpio_a and self.lev_b == 1:
                self.callback(1)
            elif channel == self.gpio_b and self.lev_a == 1:
                self.callback(-1)
