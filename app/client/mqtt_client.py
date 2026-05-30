import json
#import subprocess

import paho.mqtt.client as mqtt


BROKER = "192.168.10.11"
PORT = 1883

USERNAME = "mqtt_user"
PASSWORD = "********"

DEVICE_ID = "ftp_server"

TOPIC_CMD_SHUTDOWN = "ftp_server/cmd/shutdown"

TOPIC_ONLINE = "ftp_server/status/online"
TOPIC_FTP_ACTIVE = "ftp_server/status/ftp_active"
TOPIC_SYNCING = "ftp_server/status/syncing"
TOPIC_STATE = "ftp_server/status/state"

DISCOVERY_TOPIC = f"homeassistant/device/{DEVICE_ID}/config"

# Device Discovery Message
def publish_discovery(client):

    payload = {
        "dev": {
            "ids": DEVICE_ID,
            "name": "FTP Server",
            "mf": "Homelab",
            "mdl": "Arch Linux FTP"
        },

        "o": {
            "name": "mqtt-ftp-client"
        },

        "cmps": {

            "online": {
                "p": "binary_sensor",
                "device_class": "connectivity",
                "value_template": "{{ value }}",
                "state_topic": TOPIC_ONLINE
            },

            "ftp_active": {
                "p": "binary_sensor",
                "value_template": "{{ value }}",
                "state_topic": TOPIC_FTP_ACTIVE
            },

            "syncing": {
                "p": "binary_sensor",
                "value_template": "{{ value }}",
                "state_topic": TOPIC_SYNCING
            },

            "state": {
                "p": "sensor",
                "state_topic": TOPIC_STATE
            }
        }
    }

    client.publish(
        DISCOVERY_TOPIC,
        json.dumps(payload),
        retain=True
    )

# Only one message is expected. Maybe this function has to be modified in case of bad message (bug).
def on_message(client, userdata, msg):

    topic = msg.topic
    payload = msg.payload.decode()

    print(f"Commande reçue : {topic} -> {payload}")

    if topic == TOPIC_CMD_SHUTDOWN:

        client.publish(
            TOPIC_STATE,
            "shutdown_requested",
            retain=True
        )

        shutdown_sequence(client)


def shutdown_sequence(client):

    client.publish(
        TOPIC_SYNCING,
        "true",
        retain=True
    )

    client.publish(
        TOPIC_STATE,
        "syncing",
        retain=True
    )

    # Exemple :
    # subprocess.run(["rsync", ...])

    time.sleep(5)

    client.publish(
        TOPIC_SYNCING,
        "false",
        retain=True
    )

    client.publish(
        TOPIC_STATE,
        "shut_down",
        retain=True
    )

    # subprocess.run(["shutdown", "-h", "now"])


# MQTT Initialization
client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.username_pw_set(
    USERNAME,
    PASSWORD
)

client.will_set(
    TOPIC_ONLINE,
    payload="false",
    qos=1,
    retain=True
)

client.on_message = on_message

client.connect(
    BROKER,
    PORT,
    60
)


publish_discovery(client)

client.publish(
    TOPIC_ONLINE,
    "true",
    retain=True
)

client.publish(
    TOPIC_FTP_ACTIVE,
    "true",
    retain=True
)

client.publish(
    TOPIC_STATE,
    "running",
    retain=True
)

client.subscribe(
    TOPIC_CMD_SHUTDOWN
)

client.loop_start()


publish_discovery(client)

client.publish(
    TOPIC_ONLINE,
    "true",
    retain=True
)

client.publish(
    TOPIC_FTP_ACTIVE,
    "true",
    retain=True
)

client.publish(
    TOPIC_STATE,
    "running",
    retain=True
)

client.subscribe(
    TOPIC_CMD_SHUTDOWN
)

client.loop_start()
