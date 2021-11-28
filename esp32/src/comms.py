import uasyncio as asyncio
from umqtt.simple2 import MQTTClient

import access


class Client:
    callback = None

    def __init__(self, topic="mopidy/i/#"):
        self.topic = topic
        self.mqtt = MQTTClient(
            b"esp32_ctrl", access.HOST, keepalive=5, socket_timeout=15
        )
        self.mqtt.set_callback(self._on_msg)
        self._pull_task = None

    def start(self):
        print("Connecting to broker...")
        self.mqtt.connect(clean_session=True)
        print("Connected to MQTT broker.")
        self.mqtt.subscribe(self.topic)
        print("Subscribed to topic.")
        
        loop = asyncio.get_event_loop()
        self._pull_task = loop.create_task(self._puller())
        return True

    def stop(self):
        if self._pull_task:
            self._pull_task.cancel()
            self._pull_task = None
        self.mqtt.disconnect()

    def _on_msg(self, topic, msg, retain, dup):
        cmd = topic.decode('utf8').split('/')[-1]
        msg = msg.decode('ut8')

        if self.callback:
            self.callback(cmd, msg)
        else:
            print((cmd, msg))
            
    async def _puller(self):
        print("Starting pulling.")
        try:
            while True:
                self.mqtt.check_msg()
                asyncio.sleep_ms(50)
        except CancelledError:
            print("Stopping pulling.")

    def send(self, topic, msg):
        self.mqtt.publish(topic.encode('utf8'), msg.encode('utf8'))
