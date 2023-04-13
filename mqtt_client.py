import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(self, mqtt_address="localhost", mqtt_port=1883, mqtt_client_id="session-iot"):
        self.address = mqtt_address
        self.port = mqtt_port
        self.client_id = mqtt_client_id
        self.topic = None
        self.message_handler = None
        self.connect_handler = None
        self.client = mqtt.Client(self.client_id, clean_session=False)

    def start(self, connect_handler=None, message_handler=None, topic="#"):
        print(f"Connecting to {self.address}:{self.port}")

        self.topic = topic
        self.message_handler = message_handler
        self.connect_handler = connect_handler
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.address, self.port, 60)

        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, topic, payload):
        print(f"<- {topic} | {payload}")
        self.client.publish(topic, payload)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.client.subscribe(self.topic)
        if self.connect_handler:
            self.connect_handler()

    def on_message(self, client, userdata, message):
        if self.message_handler:
            self.message_handler(message)
        else:
            print(f"-> {message.topic} | {message.payload}")
