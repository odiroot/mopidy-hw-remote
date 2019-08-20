import logging
import socket

from paho.mqtt import client as mqtt


log = logging.getLogger(__name__)


class MopidyClient():
    def __init__(
            self, host='localhost', port=1883, topic='mopidy', callback=None):
        self.host = host
        self.port = port
        self.topic = topic
        self.callback = callback  # XXX: Dirty!

        self.client = mqtt.Client(
            client_id='remote-{}'.format(socket.gethostname()),
            clean_session=True)

        # React to events from MQTT broker.
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def start(self):
        log.debug('Connecting to MQTT broker at %s:%s', self.host, self.port)
        self.client.connect_async(host=self.host, port=self.port)

        self.client.loop_start()
        log.debug('Started MQTT communication loop.')

    def stop(self):
        self.client.disconnect()
        log.debug('Disconnected from MQTT broker')

    def _on_connect(self, client, userdata, flags, rc):
        log.info('Successfully connected to MQTT broker, result: %s', rc)

        # Follow playback state.
        full_topic = '{}/i/#'.format(self.topic)
        result, _ = self.client.subscribe(full_topic)
        if result == mqtt.MQTT_ERR_SUCCESS:
            log.debug('Subscribed to MQTT topic: %s', full_topic)
        else:
            log.warn('Failed to subscribe to MQTT topic: %s, result: %s',
                     full_topic, result)

    def _on_message(self, client, userdata, message):
        topic = message.topic.split('/')[-1]
        log.debug(
            'Received a MQTT message: %s on topic: %s', message.payload, topic)
        if self.callback:
            self.callback(topic, message.payload.decode('utf-8', 'replace'))

    def publish(self, subtopic, value):
        full_topic = '{}/c/{}'.format(self.topic, subtopic)

        log.debug('Publishing: %s to MQTT topic: %s', value, full_topic)
        return self.client.publish(topic=full_topic, payload=value)

    def toggle(self):
        return self.publish(subtopic='plb', value='toggle')

    def volume_inc(self, value=1):
        return self.publish(subtopic='vol', value='+{}'.format(value))

    def volume_dec(self, value=1):
        return self.publish(subtopic='vol', value='-{}'.format(value))
