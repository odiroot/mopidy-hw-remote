import time
from machine import I2C, Pin, Timer

import font6 as font
from ssd1306 import SSD1306_I2C
from writer import Writer


WIDTH = const(128)
HEIGHT = const(64)
CONTRAST = const(100)
SDA_PIN = const(4)
SCL_PIN = const(15)
RST_PIN = const(16)
I2C_FREQ = const(400000)
TIMER_FREQ = const(5000)
SS_DELAY = const(60)  # Screensaver.
MODAL_ROW = const(25)
MODAL_TIME = const(2000)  # Modal "hanging" time.


class Display:
    _on = True  # Display powered indicator.
    _ls = None  # Last show command timestamp.
    _ti = Timer(-1)  # Screensaver timer.
    _tm = Timer(-2)  # Modal mode timer.
    _im = False   # Modal mode indicator.
    _ba = None  # Backup of previous screen.

    def __init__(self, verbose=False):
        self.verbose = verbose

        # Immediately attach the display to I2C bus.
        Pin(RST_PIN, Pin.OUT, value=1)
        # First hardware I2C bus.
        bus = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=I2C_FREQ)
        self.dev = SSD1306_I2C(WIDTH, HEIGHT, i2c=bus)
        # Let the SSD last longer.
        self.dev.contrast(CONTRAST)
        # Prepare backup buffer.
        self._ba = bytearray(len(self.dev.buffer))

        # Reset virtual display state if affected before.
        Writer.set_textpos(self.dev, 0, 0)
        self.wri = Writer(device=self.dev, font=font, verbose=verbose)
        # Wrap long lines instead of trimming but don't allow to scroll
        # past the end of the screen.
        self.wri.set_clip(row_clip=False, col_clip=True, wrap=True)

    def start(self):
        self._ti.init(
            period=TIMER_FREQ, mode=Timer.PERIODIC, callback=self._on_timer)

    def stop(self):
        self._ti.deinit()
        self._tm.deinit()

    def _on_timer(self, _):
        if not self._on:  # Already turned off.
            return
        # Last refresh was long ago.
        if time.time() - self._ls > SS_DELAY:
            if self.verbose:
                print('Shutting down display')
            self.dev.poweroff()  # Saving power and OLED panel.
            self._on = False

    def show(self):
        self._ls = time.time()
        # Screensaver was enabled before.
        if not self._on:
            self._on = True
            self.dev.poweron()

        # Display the buffer content.
        self.dev.show()

    def text(self, s, modal=False):
        if modal:
            # Prepare for modal.
            self._modal_on()
            # Center on display.
            Writer.set_textpos(self.dev, MODAL_ROW, 0)
        else:
            # Reset previous modal state but don't draw old content.
            self._modal_off(restore=False)
            # Return the cursor to the beginning.
            Writer.set_textpos(self.dev, 0, 0)

        # Start with clean slate.
        self.dev.fill(0)
        # Draw the actual content.
        self.wri.printstring(s)
        # Send drawing commands to the screen.
        self.show()

    def _modal_on(self):
        # Only if this is first level modal (non-stacked).
        if not self._im:
            self._im = True
            # Backup current display state.
            self._ba[:] = self.dev.buffer

        # Doh't hide the modal too quickly when stacked.
        self._tm.deinit()
        # After some time, go back.
        self._tm.init(
            period=MODAL_TIME, mode=Timer.ONE_SHOT, callback=self._modal_off)

    def _modal_off(self, timer=None, restore=True):
        if not self._im:  # Outside of modal mode.
            return

        # Exit modal mode.
        self._im = None

        if restore:
            # Immediately display backed up screen.
            self.dev.buffer[:] = self._ba
            self.show()
