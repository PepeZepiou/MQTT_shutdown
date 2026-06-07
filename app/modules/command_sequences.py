import config.settings as settings
import subprocess

# All command published by Home Assistant must have a function here.
# In container, create a file in a shared folder. A .path service on host check for it, and run privilegied command outside container.



# Shutdown request :
def shutdown_sequence(client):
    client.publish(settings.TOPIC_STATE, "shutting_down", retain=True)
    client.publish(settings.TOPIC_EVENT, "shutting_down_requested", retain=False)
    # Command used in container
    #with open("/shared/commands/shutdown.request", "w") as f:
    #    f.write("shutdown")
    # Command used in dev with python
    subprocess.run(["shutdown", "-h", "now"])
