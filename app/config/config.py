import time
import os
import subprocess

BROKER = os.getenv("MQTT_ADDRESS")
PORT = int(os.getenv("MQTT_PORT"))

USERNAME = os.getenv("MQTT_USER")
PASSWORD = os.getenv("MQTT_PASSWORD")

DEVICE_ID = os.getenv("DEVICE_ID")
DEVICE_NAME = os.getenv("DEVICE_NAME")
DEVICE_MANUFACTURER = os.getenv("DEVICE_MANUFACTURER")
DEVICE_MODEL = os.getenv("DEVICE_MODEL")

TOPIC_CMD_SHUTDOWN = f"{DEVICE_ID}/cmd/shutdown"

TOPIC_ONLINE = f"{DEVICE_ID}/status/availability_topic"
TOPIC_FTP_ACTIVE = f"{DEVICE_ID}/status/ftp_active"
TOPIC_SYNCING = f"{DEVICE_ID}/status/syncing"
TOPIC_STATE = f"{DEVICE_ID}/status/state"

DISCOVERY_TOPIC = f"homeassistant/device/{DEVICE_ID}/config"

DEVICE_DISCOVERY_PAYLOAD = {
        "dev": {
            "ids": DEVICE_ID,
            "name": DEVICE_NAME,
            "mf": DEVICE_MANUFACTURER,
            "mdl": DEVICE_MODEL
        },

        "o": {
            "name": "mqtt2shutdown"
        },

        "cmps": {

            "online": {
                "p": "binary_sensor",
                "device_class": "connectivity",
                "value_template": "{{ value }}",
                "state_topic": TOPIC_ONLINE
            },

            "state": {
                "p": "sensor",
                "state_topic": TOPIC_STATE
            }
        }
    }

def shutdown_sequence(client):

    client.publish(
        TOPIC_STATE,
        "shutting_down",
        retain=True
    )

    # Do  something before shutting down:
    # subprocess.run(["rsync", ...])

    time.sleep(5)

    client.publish(
        TOPIC_STATE,
        "shut_down",
        retain=True
    )

     subprocess.run(["shutdown", "-h", "now"])
    # Normaly, TOPIC_ONLINE message will be send by broker when shutting down will produce connexion lost (Last Will Testtament).
 


def publish_state(client):
        client.publish(
            TOPIC_ONLINE,
            "online",
            retain=True
        )

        client.publish(
            TOPIC_STATE,
            "running",
            retain=True
        )
