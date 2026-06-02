import paho.mqtt.client as mqtt
import config.settings as settings
from modules.main_func import main
from modules.basic_func import on_message, on_connect
        

# MQTT Initialization
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(settings.USERNAME, settings.PASSWORD)
client.will_set(settings.TOPIC_ONLINE, payload="OFF", qos=1, retain=True)
client.reconnect_delay_set(min_delay=5, max_delay=60)
client.on_message = on_message
client.on_connect = on_connect

# MQTT Connexion
client.connect(settings.BROKER, settings.PORT, 60)

# Start MQTT Thread
client.loop_start()

# Start main loop
main(client)

