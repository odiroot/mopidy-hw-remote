from .config import BASE_URL

try:
    import requests
except ImportError:
    import urequests as requests


RPC_URL = BASE_URL + "/mopidy/rpc"


def make_request(method, params=None):
    response = requests.post(RPC_URL, json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or [],
    })

    if(response.status_code == 200):
        return response.json()["result"]


def get_state():
    return make_request("core.playback.get_state")


def get_track():
    track = make_request("core.playback.get_current_track")
    if not track:
        return None

    # Metadata can have different forms.
    # * Radio stream / SomaFM.
    if "comment" in track:
        return track["comment"]

    # * Spotify / GMusic song.
    if "name" in track and "artists" in track:
        # Ignore further artists :(.
        return " - ".join(
            (track["artists"][0]["name"], track["name"], )
        )

    # * More?
    assert False


def get_volume():
    return make_request("core.playback.get_volume")


def toggle_state():
    state = get_state()

    if state == "playing":
        make_request("core.playback.pause")
    elif state == "paused":
        make_request("core.playback.play")

    # Stopped or unknown, ignore.


def next_track():
    make_request("core.playback.next")


def previous_track():
    make_request("core.playback.previous")


def volume_up():
    volume = get_volume()
    new_val = min((volume + 10, 100))

    make_request("core.playback.set_volume", [new_val])


def volume_down():
    volume = get_volume()
    new_val = max((volume - 10, 0))

    make_request("core.playback.set_volume", [new_val])
