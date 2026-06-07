import config.settings as settings
from modules.command_sequences import shutdown_sequence
import time
import json



# Check this function utility.
def heartbeat_loop(client):
    while True:
        client.publish(settings.TOPIC_HEARTBEAT, datetime.now(timezone.utc).isoformat(), retain=False)
        time.sleep(10)



# Function used at connexion to mqtt broker.
# Send the discovery message which will configure device on Home ASSISTANT
# And send this activity as an event.
def publish_discovery(client):
    payload = settings.DEVICE_DISCOVERY_PAYLOAD
    client.publish(settings.DISCOVERY_TOPIC, json.dumps(payload), retain=True)
    client.publish(settings.TOPIC_EVENT, "discovery published", retain=False)



# Function used just at connexion to mqtt broker, just after publication of discovery message.
# Publish normal initials state.
def publish_state(client):
    client.publish(settings.TOPIC_ONLINE, "ON", retain=True)
    client.publish(settings.TOPIC_UPTIME, datetime.now(timezone.utc).isoformat(), retain=True) 
    client.publish(settings.TOPIC_STATE, "running", retain=True)
    client.publish(settings.TOPIC_EVENT, "state published", retain=False)
    client.publish(settings.TOPIC_ERROR, "none", retain=False)



# Function used in the main loop.
# Idea is to publish an heartbeat. With this, it's possible to raise an alarm in Home assistant if broker shutdown.
def publish_heartbeat(client):
    client.publish(settings.TOPIC_HEARTBEAT, str(int(time.time())), retain=False)


# Function used in main loop.
# Publish on error topic if an error is catched by "try:/except:"
def publish_error(client, msg):
    client.publish(settings.TOPIC_ERROR, msg, retain=False)



# Usual callback for paho thread.
# At connection, send discovery message, publish state and suscribe to command topic
def on_connect(client, userdata, flags, reason_code, properties):
    publish_discovery(client)
    publish_state(client)
    client.subscribe(settings.TOPIC_CMD_SHUTDOWN)



# Usual callback for paho thread.
# For the moment, any message published on command topic initiate shutdown sequence.
# In future, could initiate restart device, restart machine, acknowledge error message...
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == settings.TOPIC_CMD_SHUTDOWN:
        shutdown_sequence(client)
