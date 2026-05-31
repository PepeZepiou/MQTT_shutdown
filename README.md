# MQTT_shutdown
Trying to create a docker which will connect to Home Assistant broker, publish online status and subscribe to receive remote shutdown signal.

I would like to create a generic image, so conf will be generate at launch. So command will be something like :

docker run \
-e MQTT_ADDRESS=192.168.11.11 \
-e MQTT_PORT=1883
-e MQTT_USER=mqtt_user \
-e MQTT_PASSWORD=xxxxx \
-e DEVICE_ID=FTP_SERVER \
-e DEVICE_NAME='FTP Server' \
-e DEVICE_MANUFACTURER=Homelab \
-e DEVICE_MODEL='Arch Linux vstpd' \
mqtt_client

For the momemt, docker could not work. I will have to implement communication between host and container to shutdown.

I'm trying to improve model to be more OT like (security, error proof, aknowledgement ...). It's usefull, but interesting.

I need to implement TLS, timestamp with control on shutdown command to avoid replay, avoid double command (if state == shutting_down; return), ...

I would like to implement timestamp on event message.

An error topic has been setup, but I don't know yet how to use it in this configuration. But it can be usefull in DIY sensor.
