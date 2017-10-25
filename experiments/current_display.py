#!/usr/bin/env python2.7
from mpdc.main import get_state, get_track, get_volume
from text_wrap import wrap_cut, device, canvas, write_line
from time import sleep


def update_status(drawer):
    state = (get_state() or "").capitalize()
    volume = u"%3d%%" % get_volume()
    # Pack the line.
    line = state.ljust(12) + volume

    write_line(drawer, line, row=0)


def update_track(drawer):
    track = get_track() or ""
    track = wrap_cut(track, max_lines=4)

    for li, line in enumerate(track):
        write_line(drawer, line, row=li + 2)


def main():
    while True:
        with canvas(device) as draw:
            update_status(draw)
            update_track(draw)

        sleep(5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
