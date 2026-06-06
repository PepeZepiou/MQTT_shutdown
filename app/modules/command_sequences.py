import config.settings as settings
import subprocess

def shutdown_sequence(client):
    client.publish(settings.TOPIC_STATE, "shutting_down", retain=True)
    client.publish(settings.TOPIC_EVENT, "shutting_down_requested", retain=False)
    # Command used in container
    #with open("/shared/commands/shutdown.request", "w") as f:
    #    f.write("shutdown")
    # Command used in dev with python
    subprocess.run(["shutdown", "-h", "now"])
