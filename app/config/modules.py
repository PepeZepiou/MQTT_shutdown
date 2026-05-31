import config
import import subprocess
import json

def shutdown_sequence(client):
    client.publish(
        config.TOPIC_STATE,
        "shutting_down",
        retain=True
    )
    # Do  something before shutting down:
    # subprocess.run(["rsync", ...])
    client.publish(
        config.TOPIC_STATE,
        "shut_down",
        retain=True
    )
    subprocess.run(["shutdown", "-h", "now"])
    # This command will not work inside a container... Have to be modified with something like:
    #with open("/run/shutdown_request", "w") as f:
    #  f.write("1")
    # and a script checking this on the host.

 

def publish_state(client):
        client.publish(
            config.TOPIC_ONLINE,
            "ON",
            retain=True
        )
        client.publish(
            config.TOPIC_STATE,
            "running",
            retain=True
        )



def publish_discovery(client):
    payload = DEVICE_DISCOVERY_PAYLOAD
    client.publish(
        config.DISCOVERY_TOPIC,
        json.dumps(payload),
        retain=True
    )




def on_connect(client, userdata, flags, reason_code, properties):
    publish_discovery(client)
    publish_state(client)
    client.subscribe(config.TOPIC_CMD_SHUTDOWN)



def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == config.TOPIC_CMD_SHUTDOWN:
        client.publish(
            config.TOPIC_STATE,
            "shutdown_requested",
            retain=True
        )
        shutdown_sequence(client)
