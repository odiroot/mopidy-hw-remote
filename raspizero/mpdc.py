import logging
from time import time
from uuid import uuid4

from requests import Session

from config import VOLUME_STEP


log = logging.getLogger(__name__)

RPC_URL = 'http://{hostname}:{port}/mopidy/rpc'


class MopidyClient():
    def __init__(self, hostname='localhost', port=6680):
        self._url = RPC_URL.format(hostname=hostname, port=port)
        self._session = Session()

    def rpc(self, method, params=None):
        start = time()
        response = self._session.post(self._url, json={
            'jsonrpc': '2.0',
            'id': str(uuid4()),
            'method': method,
            'params': params or {}
        })
        duration = time() - start

        log.debug('Finished `%s` call in %.3fs', method, duration)
        response.raise_for_status()

        return response.json()['result']

    def get_state(self):
        return self.rpc('core.playback.get_state')

    def get_current(self):
        track = self.rpc('core.playback.get_current_track')
        if not track:
            return None

        # Metadata can have different forms.
        # * Radio stream / SomaFM.
        if 'comment' in track:
            return track['comment']

        # * Spotify / GMusic song.
        if 'name' in track and 'artists' in track:
            # Ignore further artists :(.
            return ' - '.join(
                (track['artists'][0]['name'], track['name'], )
            )

        # Poorest version.
        if 'name' in track:
            return track['name']

        assert False, track

    def get_volume(self):
        return self.rpc('core.playback.get_volume')

    def volume_inc(self):
        volume = self.get_volume()
        volume = min((volume + VOLUME_STEP, 100))
        self.rpc('core.playback.set_volume', [volume])

        return volume

    def volume_dec(self):
        volume = self.get_volume()
        volume = max((volume - VOLUME_STEP, 1))
        self.rpc('core.playback.set_volume', [volume])

        return volume

    def toggle(self):
        state = self.get_state()
        if state == 'playing':
            self.rpc('core.playback.pause')
        elif state == 'paused':
            self.rpc('core.playback.play')
