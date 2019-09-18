from os import getenv


# General configuration.
DEBUG = getenv('DEBUG') == '1'  # For verbose logging.

# Rotary encoder configuration.
PIN_A_NUM = getenv('PIN_A', 15)  # GPIO pin for signal A
PIN_B_NUM = getenv('PIN_B', 14)  # GPIO pin for signal B
PIN_BUT_NUM = getenv('PIN_BUTTON', 18)  # GPIO pin for push button.

# MPD configuration.
MQTT_HOST = getenv('MQTT_HOST', 'localhost')  # Hostname of MQTT broker.
MQTT_TOPIC = getenv('MQTT_TOPIC', 'mopidy')

# Volume control configuration.
VOLUME_STEP = 4

# Display configuration.
I2C_PORT = 1
I2C_ADDRESS = 0x3C
FONT_NAME = getenv('FONT_NAME', 'ProggyTiny.ttf')
FONT_SIZE = int(getenv('FONT_SIZE', 16))
DISPLAY_TIMEOUT = int(getenv('DISPLAY_TIMEOUT', 30))
