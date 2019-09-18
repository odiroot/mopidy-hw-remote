import logging
from os.path import abspath, dirname, join
from threading import Timer
from warnings import warn

from luma.core.error import Error
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont


HERE = abspath(dirname(__file__))
FONT_DIR = join(HERE, 'fonts')

log = logging.getLogger(__name__)


class Display(object):
    def __init__(
            self, address, port=1, font_name=None, font_size=14,
            timeout=10):
        self.port = port
        self.address = address
        self.device = None
        self.font = None
        self.timeout = timeout
        self._timer = None  # Screen-saver timer.

        # Override default font with a nicer one.
        if font_name and font_size:
            self.font = ImageFont.truetype(
                join(FONT_DIR, font_name), font_size)

    def start(self):
        try:
            serial = i2c(port=self.port, address=self.address)
            # Initialise with default 128x64 matrix, mono.
            self.device = ssd1306(serial)
        except Error:
            log.warn(
                'Could not connect to i2c display: %s:%s',
                self.port, self.address)
            try:  # Try display emulator.
                from luma.emulator.device import pygame
                self.device = pygame(
                    width=128, height=64,
                    frame_rate=10,
                    scale=4,
                    transform='identity')
            except (Error, ImportError):
                log.error('Could not find any display to use.')
        self.text('Display ready!')

    def stop(self):
        log.info('Shutting down external display')
        if self.device:
            self.device.hide()

    def schedule_screen_saver(self):
        """Turns the display off after period of inactivity."""
        log.debug('Scheduling next display power off')
        # Another consecutive call: cancel previous countdown to saving.
        if self._timer:
            self._timer.cancel()

        # Setup next timer to execute at trailing edge.
        self._timer = Timer(interval=self.timeout, function=self.stop)
        # Run screen saver after waiting time passed.
        self._timer.start()

    def text(self, s):
        if not self.device:
            warn('Display device not initialised')
            return

        with canvas(self.device) as draw:
            coords = (1, 0,)
            draw.multiline_text(
                coords, s, fill='white', font=self.font, spacing=1)
        self.device.show()

        self.schedule_screen_saver()
