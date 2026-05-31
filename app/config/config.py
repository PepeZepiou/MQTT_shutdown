import time
import os
import subprocess

# BROKER INFORMATIONS
BROKER = os.getenv("MQTT_ADDRESS", "192.168.1.11")
PORT = int(os.getenv("MQTT_PORT", "1883"))
USERNAME = os.getenv("MQTT_USER", "mqtt_user")
PASSWORD = os.getenv("MQTT_PASSWORD")

# DEVICE INFORMATIONS
DEVICE_ID = os.getenv("DEVICE_ID")
DEVICE_NAME = os.getenv("DEVICE_NAME")
DEVICE_MANUFACTURER = os.getenv("DEVICE_MANUFACTURER", "Home_made")
DEVICE_MODEL = os.getenv("DEVICE_MODEL", "Model_1")

# TOPICS
# COMMAND TOPIC
TOPIC_CMD_SHUTDOWN = f"MQTT_Shutdown/{DEVICE_ID}/cmd/shutdown"
# TELEMETRY TOPICS
TOPIC_ONLINE = f"MQTT_Shutdown/{DEVICE_ID}/telemetry/availability"
TOPIC_HEARTBEAT = f"MQTT_Shutdown/{DEVICE_ID}/telemetry/heartbeat"
#TOPIC_UPTIME = f"MQTT_Shutdown/{DEVICE_ID}/telemetry/uptime"
# EVENTS TOPICS
TOPIC_STATE = f"MQTT_Shutdown/{DEVICE_ID}/event/state"
TOPIC_ERROR = f"MQTT_Shutdown/{DEVICE_ID}/event/error"
# HOME ASSISTANT AUTO-DISCOVERY TOPIC
DISCOVERY_TOPIC = f"homeassistant/device/{DEVICE_ID}/config"

# JSON PAYLOAD FOR MQTT INTEGRATION AUTO-DISCOVERY
# NOTES : ERROR AND UPTIME WILL NOT BE USED FOR THE MOMENT
# I HAVE TO FIND A WAY TO CHEK FOR ERRORS
# AND I HAVE TO CHECK HOW TO REPRESENT TIME IN MQTT INTEGRATION
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
                "state_topic": TOPIC_ONLINE,
                "unique_id": f"{DEVICE_ID}_connectivity_sensor"
            },
            "state": {
                "p": "sensor",
                "state_topic": TOPIC_STATE,
                "unique_id": f"{DEVICE_ID}_state_sensor"
            },
            "shutdown": {
                "p": "button",
                "command_topic": TOPIC_CMD_SHUTDOWN,
                "unique_id": f"{DEVICE_ID}_cmd_button"
            },
            "heartbeat": {
                "p": "sensor",
                "device_class": "timestamp",
                "value_template": "{{ as_datetime(value) }}",
                "unique_id": f"{DEVICE_ID}_heartbeat_sensor",
                "state_topic": TOPIC_HEARTBEAT
            },
            "error": {
                "p": "sensor",
                "state_topic": TOPIC_ERROR,
                "unique_id": f"{DEVICE_ID}_error_sensor"
            },
            "uptime": {
                "p": "sensor",
                "device_class": "timestamp",
                "value_template": "{{ as_datetime(value) }}",
                "unique_id": f"{DEVICE_ID}_uptime_sensor",
                "state_topic": TOPIC_UPTIME
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
            "ON",
            retain=True
        )

        client.publish(
            TOPIC_STATE,
            "running",
            retain=True
        )
