# BROKER INFORMATIONS
BROKER = os.getenv("MQTT_ADDRESS", "192.168.1.11")
PORT = int(os.getenv("MQTT_PORT", "1883"))
USERNAME = os.getenv("MQTT_USER", "mqtt_user")
PASSWORD = os.getenv("MQTT_PASSWORD")

# DEVICE INFORMATIONS
DEVICE_ID = os.getenv("DEVICE_ID")
DEVICE_NAME = os.getenv("DEVICE_NAME")
DEVICE_MANUFACTURER = os.getenv("DEVICE_MANUFACTURER", "Home_made")
DEVICE_MODEL = os.getenv("DEVICE_MODEL", "Model_1")

# TOPICS
# COMMAND TOPIC
TOPIC_CMD_SHUTDOWN = f"mqtt2shutdown/{DEVICE_ID}/cmd/shutdown"
# TELEMETRY TOPICS
TOPIC_ONLINE = f"mqtt2shutdown/{DEVICE_ID}/telemetry/availability"
TOPIC_HEARTBEAT = f"mqtt2shutdown/{DEVICE_ID}/telemetry/heartbeat"
TOPIC_UPTIME = f"mqtt2shutdown/{DEVICE_ID}/telemetry/uptime"
TOPIC_STATE = f"mqtt2shutdown/{DEVICE_ID}/event/state"
# EVENTS TOPICS
TOPIC_EVENT = f"mqtt2shutdown/{DEVICE_ID}/event/event"
TOPIC_ERROR = f"mqtt2shutdown/{DEVICE_ID}/event/error"        # THIS SHOULD BE USED LATER IN OT LIKE DIY SENSORS
# HOME ASSISTANT AUTO-DISCOVERY TOPIC
DISCOVERY_TOPIC = f"homeassistant/device/{DEVICE_ID}/config"
