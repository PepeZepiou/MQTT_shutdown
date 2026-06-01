import config.config as config
import subprocess

def shutdown_sequence(client):
    client.publish(config.TOPIC_STATE, "shutting_down", retain=True)
    client.publish(config.TOPIC_EVENT, "shutting_down_requested", retain=False)
    # Command used in container
    #with open("/shutdown/request", "w") as f:
    #    f.write("shutdown")
    # Command used in dev with python
    subprocess.run(["shutdown", "-h", "now"])
