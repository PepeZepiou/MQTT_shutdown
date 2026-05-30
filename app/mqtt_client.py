import json
#import subprocess

import paho.mqtt.client as mqtt
from config.config import *


# Device Discovery Message
def publish_discovery(client):

    payload = DEVICE_DISCOVERY_PAYLOAD

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
    payload="offline",
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

publish_state(client)

client.subscribe(
    TOPIC_CMD_SHUTDOWN
)

client.loop_forever()
