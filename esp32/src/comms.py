import uasyncio as asyncio
from mqtt_as import config, MQTTClient

import access


class Client:
    callback = None

    def __init__(self, topic, verbose=False):
        self.topic = topic
        self.verbose = verbose
        # Configure the MQTT library for current board.
        config.update(
            server=access.HOST,
            ssid=access.SSID,
            wifi_pw=access.PASSWORD,
            connect_coro=self._on_conn,
            subs_cb=self._on_msg,
        )
        self.mqtt = MQTTClient(config)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.mqtt.connect())

    def stop(self):
        # Prevent LmacRxBlk:1 errors.
        self.mqtt.close()

    async def _on_conn(self, client):
        if self.verbose:
            print('Connected to broker. Subscribing to: %s.' % self.topic)
        await client.subscribe(self.topic)

    def _on_msg(self, topic, msg, _):
        cmd = topic.decode('utf8').split('/')[-1]
        msg = msg.decode('ut8')

        if self.callback:
            self.callback(cmd, msg)
        else:
            print((cmd, msg))
