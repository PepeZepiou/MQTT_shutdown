import modules.basic_func as func
import time

# The main function is a loop.
# I choose this architecture to avoid to interupt paho thread with a sleep used for heartbeat publication.
# Could integrate anything later, but for the moment just publish the heartbeat each 30s 
# and publish on error topic in case of.

def main(client):
    last_heartbeat = 0
    while True:
        try:
            now = time.time()
            if now - last_heartbeat > 30:
                func.publish_heartbeat(client)
                last_heartbeat = now
        except Exception as e:
            func.publish_error(client, f"Error in main loop: {e}", retain=False)

        time.sleep(1)
