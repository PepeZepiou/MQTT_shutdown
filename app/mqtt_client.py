import paho.mqtt.client as mqtt
import config.config as config
import config.modules as modules
        

# MQTT Initialization
client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)
client.username_pw_set(
    config.USERNAME,
    config.PASSWORD
)
client.will_set(
    config.TOPIC_ONLINE,
    payload="OFF",
    qos=1,
    retain=True
)
client.reconnect_delay_set(min_delay=5, max_delay=60)
client.on_message = modules.on_message
client.on_connect = modules.on_connect

client.connect(
    config.BROKER,
    config.PORT,
    60
)

client.loop_forever()
