# MQTT_shutdown
Trying to create a docker which will connect to Home Assistant broker, publish online status and subscribe to receive remote shutdown signal.

I would like to create a generic image, so conf will be generate at launch. So command will be something like :

docker run \
--name mqtt2shutdown \
-v /opt/mqtt2shutdown/commands:/shared/commands \
-e MQTT_ADDRESS=192.168.11.11 \
-e MQTT_PORT=1883 \
-e MQTT_USER=mqtt_user \
-e MQTT_PASSWORD=xxxxx \
-e DEVICE_ID=FTP_SERVER \
-e DEVICE_NAME='FTP Server' \
-e DEVICE_MANUFACTURER=Homelab \
-e DEVICE_MODEL='Arch Linux vstpd' \
mqtt_client

Container will create a MQTT client, communicate with  MQTT broker, and write in file /shared/commands/shutdown.request.
A systemd unit .service launch container at startup, a .path unit check if something exist in /shared/commands/shutdown.request, and start .service which launch /usr/local/bin/shutdown-handler.sh.
This one will remove file in /shared/commands/, then execute shutdown sequence.

I'm trying to improve model to be more OT like (security, error proof, aknowledgement ...). It's usefull, but interesting.

I need to implement TLS, timestamp with control on shutdown command to avoid replay, avoid double command (if state == shutting_down; return), ...

I would like to implement timestamp on event message.

An error topic has been setup, but I don't know yet how to use it in this configuration. But it can be usefull in DIY sensor.


USAGE:

Create shared folder:
mkdir /opt/mqtt2shutdown/commands/

Copy services:
cp ./systemd/* /etc/systemd/system/
chmod +x /etc/systemd/system/...

Enable services:
systemctl enable ...
