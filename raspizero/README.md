# Raspberry-Pi-based Mopidy controller prototype

**Note**: This project assumes your Mopidy installation uses
          [MQTT control backend](https://github.com/odiroot/mopidy-mqtt).

## Components

* Raspberry Pi Zero W board.
* SSD1306 OLED, I²C-based 128×64 display.
* EVE-PDBRL408B rotary encoder with switch.

## Software stack

* Python 3.6.
* `luma.oled` (display driving).
  - `luma.emulator` (emulating display in development).
* `RPi.GPIO` (interfacing with hardware inputs).
  - `raspberry-gpio-emulator` (emulating GPIO inputs in development).
* `paho.mqtt` (MQTT communication).

## Hardware design

Look [here!](./docs/design.md)

# Quickstart

## Installation
Latest stable version from _Python Package Index_:

    $ pip3 install mopidy-rpi-remote

Latest unstable version from _Github_:

    $ pip3 install -e git+https://github.com/odiroot/mopidy-hw-remote.git/#egg=mopidy_rpi_remote&subdirectory=raspizero

## Running
Verify you can run the main script in the foreground:

    $ mopidy_remote

If everything works fine setup the _systemd_ service:

    $ sudo cp mopidy_control.service /etc/systemd/system/mopidy_control.service
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable mopidy_control.service
    $ sudo systemctl start mopidy_control.service

## Configuration

Edit the service configuration file to adjust to your setup:

    $ sudo vi /etc/systemd/system/mopidy_control.service

Most importantly configure the _MQTT_ broker:

    Environment=MQTT_HOST=<your broker IP>

After saving the file run:

    $ sudo systemctl daemon-reload
    $ sudo systemctl restart mopidy_control.service
