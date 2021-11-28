def parse_trk(value):
    parts = value.split(';')
    if not parts:
        return None
    if len(parts) == 1:
        return parts[0]
    return ' - '.join(parts[1::-1])


class Controller:
    def __init__(self, display, client, panel):
        self.d = display
        self.c = client
        self.p = panel

        # Bind the network commands to coetroller handlers.
        self.c.callback = self.on_msg
        self.d.text('Ready to go!')

        # TODO: Refactor binding to Panel class itself.
        # Bind the button input to controller handlers.
        self.p.red.release_func(self.on_red_click)
        self.p.yellow.release_func(self.on_yellow_click)
        self.p.yellow.long_func(self.on_yellow_long)
        self.p.green.release_func(self.on_green_click)
        self.p.green.long_func(self.on_green_long)
        self.p.orange.release_func(self.on_orange_click)
        self.p.orange.long_func(self.on_orange_long)

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

    async def on_red_click(self):
        print('Toggle speakers')
        self.c.send('cmnd/speakers/power', 'toggle')

    async def on_yellow_click(self):
        print('Toggle play')
        self.c.send('mopidy/c/plb', 'toggle')

    async def on_yellow_long(self):
        print('Next track')
        self.c.send('mopidy/c/plb', 'next')

    async def on_green_click(self):
        print('Volume up')
        self.c.send('mopidy/c/vol', '+5')

    async def on_green_long(self):
        print('Volume UP!')
        self.c.send('mopidy/c/vol', '+50')

    async def on_orange_click(self):
        print('Volume down')
        self.c.send('mopidy/c/vol', '-5')

    async def on_orange_long(self):
        print('Volume DOWN!')
        self.c.send('mopidy/c/vol', '-50')
