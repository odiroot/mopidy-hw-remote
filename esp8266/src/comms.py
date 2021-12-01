from mqtt_as import config, MQTTClient

import access


MQTTClient.DEBUG = True  # Optional: print diagnostic messages


class Client:
    callback = None
    ready = False

    def __init__(self):
        config.update(
            client_id=access.CLIENT_ID,
            ssid=access.WIFI_SSID,
            wifi_pw=access.WIFI_KEY,
            server=access.BROKER_HOST,

            connect_coro=self._on_conn,
            subs_cb=self._on_msg,
            response_time=20,
        )
        self.mqtt = MQTTClient(config)

    async def start(self):
        await self.mqtt.connect()
        self.ready = True

    def stop(self):
        # Prevent LmacRxBlk:1 errors.
        self.mqtt.close()

    async def _on_conn(self, client):
        await client.subscribe(access.BROKER_TOPIC)
        print("Subscribed to topic.")

    def _on_msg(self, topic, msg, _):
        cmd = topic.decode('utf8').split('/')[-1]
        msg = msg.decode('ut8')

        if self.callback:
            self.callback(cmd, msg)
        else:
            print("Got message:", cmd, msg)

    async def send(self, topic, msg):
        if not self.ready:
            print("Not sending. No connection made.")
            return

        return await self.mqtt.publish(
            topic.encode('utf8'), msg.encode('utf8'))
