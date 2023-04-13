import json
from time import sleep


class DeviceLight:
    prefix = "shellies/shellycolorbulb-3494546B7048/"
    command_topic = f"{prefix}color/0/set"
    commands = {
        "reset": {
            "mode": "color", "turn": "on",
            "red": 0, "green": 0, "blue": 255,
            "white": 0, "gain": 5, "transition": 1000
        },
        "boiling": {
            "mode": "color", "turn": "on",
            "red": 255, "green": 0, "blue": 0,
            "white": 0, "gain": 10, "transition": 5000
        },
        "alarm1": {
            "mode": "color", "turn": "on",
            "red": 0, "green": 0, "blue": 0,
            "white": 255, "gain": 100, "transition": 1
        },
        "alarm2": {
            "mode": "color", "turn": "on",
            "red": 0, "green": 0, "blue": 0,
            "white": 10, "gain": 100, "transition": 200
        },
    }

    def __init__(self, mqtt):
        self.mqtt = mqtt

    def _send_command(self, command):
        self.mqtt.publish(self.command_topic, json.dumps(self.commands[command]))

    def reset(self):
        self._send_command("reset")

    def show_boiling(self):
        self._send_command("boiling")

    def show_alarm(self):
        for _ in range(1, 6):
            self._send_command("alarm1")
            sleep(1)
            self._send_command("alarm2")
            sleep(1)


class DeviceBoiler:
    prefix = "shellies/shellyplug-s-894233/"
    command_topic = f"{prefix}relay/0/command"
    commands = {
        "on": "on",
        "off": "off",
    }

    def __init__(self, mqtt):
        self.mqtt = mqtt
        self.relay_on = False
        self.current_power = 0

    def reset(self):
        self._send_command("on")

    def _send_command(self, command):
        self.mqtt.publish(self.command_topic, self.commands[command])

    def update(self, message):
        if message.topic.endswith("relay/0"):
            self.relay_on = True if message.payload.decode() == "on" else False
        elif message.topic.endswith("relay/0/power"):
            self.current_power = float(message.payload.decode())

