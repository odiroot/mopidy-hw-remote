# mopidy-hw-remote
Hardware-based remote controller for Mopidy instance

## Components used

* NodeMCU board (ESP8266 chip, 4M version) for production use
* Raspberry Pi Model B for development
* SSD1306 display (monochrome OLED, 128x64 pixels, I²C interface)
* EVE-PDBRL408B encoder with switch (mechanical, infinite rotation, incremental/quadrature output)

## Software

* Micropython ESP8266 distribution for production use
* Standard Python 2.7 for development / prototyping
* `ssd1306` display driver in production
* [`luma.oled`](https://github.com/rm-hull/luma.oled/) display driver in development
* `urequests` module for HTTP requests
* `machine.I2C` module for serial driver in production
* `smbus`module for serial driver in development
* `machine.Pin` module for reading input in production
* [`micropython-machine-linux`](https://github.com/turbinenreiter/micropython-machine-linux/blob/master/machine/gpio.py) or `RPi.GPIO` for reading input in development
