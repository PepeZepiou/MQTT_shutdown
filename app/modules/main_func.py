import modules.basic_func as func
import time



def main(client):
    last_heartbeat = 0
    while True:
        try:
            now = time.time()
            if now - last_heartbeat > 10:
                func.publish_heartbeat(client)
                last_heartbeat = now
        except Exception as e:
            func.publish_error(client, f"Error in main loop: {e}")

        time.sleep(1)
