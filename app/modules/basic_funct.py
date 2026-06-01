import config.config as config
import time
import json



# Check this function utility.
def heartbeat_loop(client):
    while True:
        client.publish(config.TOPIC_HEARTBEAT, datetime.now(timezone.utc).isoformat(), retain=False)
        time.sleep(10)



def publish_state(client):
    client.publish(config.TOPIC_ONLINE, "ON", retain=True)
    client.publish(config.TOPIC_STATE, "running", retain=True)
    client.publish(config.TOPIC_EVENT, "state published", retain=False)



def publish_discovery(client):
    payload = config.DEVICE_DISCOVERY_PAYLOAD
    client.publish(config.DISCOVERY_TOPIC, json.dumps(payload), retain=True)
    client.publish(config.TOPIC_EVENT, "discovery published", retain=False)



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
