#!/bin/env python3
import signal
from time import sleep, time

from mqtt_client import MqttClient
from devices import DeviceLight, DeviceBoiler


MQTT_BROKER = "session-iot.local"
TOPICS = [
    (f"{DeviceBoiler.prefix}#", 0),
    (f"{DeviceLight.prefix}#", 0),
]


class SessionIot:
    def __init__(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        self.stop_flag = False
        self.mqtt = None
        self.boiler_device = None
        self.light_device = None
        self.last_status_boiling = False
        self.boiling_start_time = None

    def run(self):
        self.mqtt = MqttClient(MQTT_BROKER)
        self.light_device = DeviceLight(self.mqtt)
        self.boiler_device = DeviceBoiler(self.mqtt)
        self.mqtt.start(connect_handler=self.reset_devices,
                        message_handler=self.mqtt_handler,
                        topic=TOPICS)
        while not self.stop_flag:
            self.update_status()
            sleep(1)

    def stop(self, *args):
        self.reset_devices()
        self.mqtt.stop()
        self.stop_flag = True

    def mqtt_handler(self, message):
        if message.topic.startswith(DeviceBoiler.prefix):
            self.boiler_device.update(message)

    def reset_devices(self):
        self.light_device.reset()
        self.boiler_device.reset()

    def update_status(self):
        boiling = True if self.boiler_device.current_power > 1000 else False
        if boiling and not self.last_status_boiling:
            self.boiling_start_time = time()
            self.last_status_boiling = True
            self.light_device.show_boiling()

        boiling_time = int(time() - self.boiling_start_time) if self.boiling_start_time else 0

        if not boiling and self.last_status_boiling:
            self.last_status_boiling = False
            self.boiling_start_time = None
            if boiling_time > 5:
                self.light_device.show_alarm()
            self.light_device.reset()

        if self.boiler_device.relay_on:
            if boiling:
                print(f"Boiling since {boiling_time} seconds with {int(self.boiler_device.current_power)} watts")
            else:
                print("Boiler idle.")
        else:
            print("Boiler disabled.")


if __name__ == '__main__':
    session = SessionIot()
    session.run()
