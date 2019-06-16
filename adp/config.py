from os import getenv


# General configuration.
DEBUG = getenv('DEBUG') == '1'  # For verbose logging.

# Rotary encoder configuration.
PIN_A_NUM = getenv('PIN_A', 15)  # GPIO pin for signal A
PIN_B_NUM = getenv('PIN_B', 14)  # GPIO pin for signal B
PIN_BUT_NUM = getenv('PIN_BUTTON', 18)  # GPIO pin for push button.

# MPD configuration.
MPD_HOST = getenv('MPD_HOST', 'localhost')  # Hostname of MPD instance.

# Volume control configuration.
VOLUME_MIN = 5
VOLUME_MAX = 99
VOLUME_INCREMENT = 1