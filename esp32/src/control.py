def parse_trk(value):
    parts = value.split(';')
    if not parts:
        return None
    if len(parts) == 1:
        return parts[0]
    return ' - '.join(parts[:2])


class Controller:
    def __init__(self, display, client):
        self.d = display
        self.c = client

        self.c.callback = self.on_msg
        self.d.text('Ready to go!')

    def on_trk(self, value):
        track = parse_trk(value)
        if not track:  # No point showing empty.
            return

        self.d.text('Now playing:\n%s' % track)

    def on_vol(self, value):
        self.d.text('Volume: %s %%' % value, modal=True)

    def on_sta(self, value):
        if value == 'stopped':
            self.d.text('Playback stopped\n\nQueue empty')
        else:
            self.d.text('State: %s' % value, modal=True)

    CMD_MAP = {
        'trk': on_trk,
        'vol': on_vol,
        'sta': on_sta,
    }

    def on_msg(self, cmd, value):
        handler = self.CMD_MAP.get(cmd)
        if not handler:
            print('Unknown command: %s', cmd)
            return

        handler(self, value)
