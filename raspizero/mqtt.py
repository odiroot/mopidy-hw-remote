import logging
import socket

from paho.mqtt import client as mqtt


log = logging.getLogger(__name__)


class MopidyClient():
    # XXX: Dirty non-authoritative state.
    _last_state = None

    def __init__(self, host='localhost', port=1883, topic='mopidy'):
        self.host = host
        self.port = port
        self.topic = topic

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
        topic = '{}/state'.format(self.topic)
        result, _ = self.client.subscribe(topic)
        if result == mqtt.MQTT_ERR_SUCCESS:
            log.debug('Subscribed to MQTT topic: %s', topic)
        else:
            log.warn('Failed to subscribe to MQTT topic: %s, result: %s',
                     topic, result)

    def _on_message(self, client, userdata, message):
        topic = message.topic.split('/')[-1]
        log.debug(
            'Received a MQTT message: %s on topic: %s', message.payload, topic)

        # Simulate toggle by remembering the last state.
        if topic == 'state':
            self._last_state = message.payload.decode('utf-8')

    def publish(self, subtopic, value):
        topic = '{}/{}'.format(self.topic, subtopic)

        log.debug('Publishing: %s to MQTT topic: %s', value, topic)
        return self.client.publish(topic=topic, payload=value)

    def toggle(self):
        if self._last_state == 'playing':
            return self.publish(subtopic='control', value='pause')
        elif self._last_state == 'paused':
            return self.publish(subtopic='control', value='resume')
        elif self._last_state == 'stopped':
            return self.publish(subtopic='control', value='play')
        else:  # Have to go with something.
            return self.publish(subtopic='info', value='state')

    def volume_inc(self):
        return self.publish(subtopic='control', value='volplus')

    def volume_dec(self):
        return self.publish(subtopic='control', value='volminus')
