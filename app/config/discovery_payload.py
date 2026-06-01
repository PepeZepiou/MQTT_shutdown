# JSON PAYLOAD FOR MQTT INTEGRATION AUTO-DISCOVERY
# NOTES : ERROR AND UPTIME WILL NOT BE USED FOR THE MOMENT
# I HAVE TO FIND A WAY TO CHEK FOR ERRORS
# AND I HAVE TO CHECK HOW TO REPRESENT TIME IN MQTT INTEGRATION
DEVICE_DISCOVERY_PAYLOAD = {
        "dev": {
            "ids": DEVICE_ID,
            "name": DEVICE_NAME,
            "mf": DEVICE_MANUFACTURER,
            "mdl": DEVICE_MODEL
        },
        "o": {
            "name": "mqtt2shutdown"
        },
        "cmps": {
            "online": {
                "p": "binary_sensor",
                "name": "Connectivity",
                "device_class": "connectivity",
                "value_template": "{{ value }}",
                "state_topic": TOPIC_ONLINE,
                "unique_id": f"{DEVICE_ID}_connectivity_sensor"
            },
            "state": {
                "p": "sensor",
                "name": "State",
                "state_topic": TOPIC_STATE,
                "unique_id": f"{DEVICE_ID}_state_sensor"
            },
            "event": {
                "p": "sensor",
                "name": "Event",
                "state_topic": TOPIC_EVENT,
                "unique_id": f"{DEVICE_ID}_event_sensor"
            },   
            "shutdown": {
                "p": "button",
                "name": "Shutdown Button",
                "command_topic": TOPIC_CMD_SHUTDOWN,
                "unique_id": f"{DEVICE_ID}_cmd_button"
            },
            "heartbeat": {
                "p": "sensor",
                "device_class": "timestamp",
                "name": "HeartBeat",
                "value_template": "{{ as_datetime(value) }}",
                "unique_id": f"{DEVICE_ID}_heartbeat_sensor",
                "state_topic": TOPIC_HEARTBEAT
            },
            "error": {
                "p": "sensor",
                "name": "Error",
                "state_topic": TOPIC_ERROR,
                "unique_id": f"{DEVICE_ID}_error_sensor"
            },
            "uptime": {
                "p": "sensor",
                "name": "Uptime",
                "device_class": "timestamp",
                "value_template": "{{ as_datetime(value) }}",
                "unique_id": f"{DEVICE_ID}_uptime_sensor",
                "state_topic": TOPIC_UPTIME
            }
        }
    }
