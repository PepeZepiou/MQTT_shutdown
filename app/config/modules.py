import config
import subprocess
import json



def shutdown_sequence(client):
    client.publish(config.TOPIC_STATE, "shutting_down", retain=True)
    client.publish(config.TOPIC_EVENT, "shutting_down_requested", retain=True)
    # Command used in container
    #with open("/shutdown/request", "w") as f:
    #    f.write("shutdown")
    # Command used in dev with python
    subprocess.run(["shutdown", "-h", "now"])



def heartbeat_loop(client):
    while True:
        client.publish(config.TOPIC_HEARTBEAT, str(int(time.time())), retain=False)
        time.sleep(10)



def publish_state(client):
    client.publish(config.TOPIC_ONLINE, "ON", retain=True)
    client.publish(config.TOPIC_STATE, "running", retain=True)
    client.publish(config.TOPIC_EVENT, "state published", retain=True)



def publish_discovery(client):
    payload = config.DEVICE_DISCOVERY_PAYLOAD
    client.publish(config.DISCOVERY_TOPIC, json.dumps(payload), retain=True)
    client.publish(config.TOPIC_EVENT, "discovery published", retain=True)



def publish_heartbeat(client):
    client.publish(config.TOPIC_HEARTBEAT, str(int(time.time())), retain=False)



def publish_error(client, msg):
    client.publish(config.TOPIC_ERROR, msg, retain=False)
    


def on_connect(client, userdata, flags, reason_code, properties):
    publish_discovery(client)
    publish_state(client)
    client.subscribe(config.TOPIC_CMD_SHUTDOWN)



def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == config.TOPIC_CMD_SHUTDOWN:
        shutdown_sequence(client)



def main(client):
    last_heartbeat = 0
    while True:
        try:
            now = time.time()
            if now - last_heartbeat > 10:
                publish_heartbeat(client)
                last_heartbeat = now
        except Exception as e:
            publish_error(client, f"Error in main loop: {e}")

        time.sleep(1)

