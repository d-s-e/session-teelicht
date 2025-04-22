# Session Teelicht (tea light)

**This repository has been moved to [Codeberg](https://codeberg.org/d-s-e/session-teelicht).**

During our hacking events we often had the problem, that someone started
the water kettle in the other room to make tea, and forgot about it while
chatting with other pople. Then they had to start the kettle again ... and
maybe forget it one more time.

To solve this, I did a small IoT-Setup, that was meant to solve this problem.

![Image of a glowing Wifi lamp and a tea cup](images/lamp.jpg)

![Image of an electric water kettle connected with a Wifi plug](images/plug.jpg)


In the default configuration the following light signals are implemented:

- **Blue:** The water kettle is idle.
- **Red:** The water kettle has been switched on and is heating.
- **White Blinking:** The water kettle has switched off, hot water should be ready.


## Required parts:

These are the parts we used. It should also work with other devices, but then you have
to adapt the MQTT commands used in the code.

- a Wifi power plug with power measurement (Shelly Plug S)
- a Wifi RGB light bulb (Shelly Duo RGBW)
- a computer to run the MQTT broker and this script (Raspberry Pi)
- a network with a wifi access point

*TODO: make device specific code configurable ...*


## Setup:

I won't go into details about the basic Raspi and IoT setup, because there is
plenty of information to find out there about those topics.

1. Setup your Raspberry Pi and install and configure an MQTT broker like
   mosquitto.
2. Setup your IoT devices for access to your Wifi and MQTT broker
3. Clone this repository into your file system:

        git clone https://github.com/d-s-e/session-teelicht.git /opt/session-teelicht

4. Create and activate the virtual environment and install the dependencies:

        cd /opt/session-teelicht
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -r requirements.txt
        deactivate

5. Create a user and install the systemd service:

        useradd -U -r -s /usr/sbin/nologin session-teelicht
        cp session-teelicht.service /etc/systemd/system/
        systemctl daemon-reload
        systemctl start session-teelicht
        systemctl enable session-teelicht


