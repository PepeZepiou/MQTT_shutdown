BROKER = "192.168.10.11"
PORT = 1883

USERNAME = "mqtt_user"
PASSWORD = "********"

DEVICE_ID = "ftp_server"

TOPIC_CMD_SHUTDOWN = f"{DEVICE_ID}/cmd/shutdown"

TOPIC_ONLINE = f"{DEVICE_ID}/status/online"
TOPIC_FTP_ACTIVE = f"{DEVICE_ID}/status/ftp_active"
TOPIC_SYNCING = f"{DEVICE_ID}/status/syncing"
TOPIC_STATE = f"{DEVICE_ID}/status/state"

DISCOVERY_TOPIC = f"homeassistant/device/{DEVICE_ID}/config"

DEVICE_DISCOVERY_PAYLOAD = {
        "dev": {
            "ids": DEVICE_ID,
            "name": "FTP Server",
            "mf": "Homelab",
            "mdl": "Arch Linux FTP"
        },

        "o": {
            "name": "mqtt-ftp-client"
        },

        "cmps": {

            "online": {
                "p": "binary_sensor",
                "device_class": "connectivity",
                "value_template": "{{ value }}",
                "state_topic": TOPIC_ONLINE
            },

            "ftp_active": {
                "p": "binary_sensor",
                "value_template": "{{ value }}",
                "state_topic": TOPIC_FTP_ACTIVE
            },

            "syncing": {
                "p": "binary_sensor",
                "value_template": "{{ value }}",
                "state_topic": TOPIC_SYNCING
            },

            "state": {
                "p": "sensor",
                "state_topic": TOPIC_STATE
            }
        }
    }

def shutdown_sequence(client):

    client.publish(
        TOPIC_SYNCING,
        "true",
        retain=True
    )

    client.publish(
        TOPIC_STATE,
        "syncing",
        retain=True
    )

    # Exemple :
    # subprocess.run(["rsync", ...])

    time.sleep(5)

    client.publish(
        TOPIC_SYNCING,
        "false",
        retain=True
    )

    client.publish(
        TOPIC_STATE,
        "shut_down",
        retain=True
    )

    # subprocess.run(["shutdown", "-h", "now"])


def publish_state(client):
        client.publish(
            TOPIC_ONLINE,
            "true",
            retain=True
        )

        client.publish(
            TOPIC_FTP_ACTIVE,
            "true",
            retain=True
        )

        client.publish(
            TOPIC_STATE,
            "running",
            retain=True
        )
