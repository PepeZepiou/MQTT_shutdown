# MQTT2Shutdown

MQTT2Shutdown is a lightweight Python application designed to expose Linux hosts to Home Assistant through MQTT Discovery.

The project runs inside a Docker container and allows Home Assistant to remotely shut down a Linux machine through MQTT commands.

The container itself never executes privileged system commands. Instead, it communicates with the host through a shared directory monitored by systemd.

This project is primarily intended for homelab environments.

---

## Features

* MQTT client based on Paho MQTT
* Home Assistant MQTT Discovery support
* Availability reporting
* Device state reporting
* Remote shutdown command
* Docker deployment
* Systemd integration
* Shared-folder based host communication
* Last Will and Testament (LWT)
* Heartbeat telemetry

---

## Architecture

```text
Home Assistant
      │
      ▼
 MQTT Broker
      │
      ▼
 MQTT2Shutdown Container
      │
      ▼
 /opt/mqtt2shutdown/commands
      │
      ▼
 mqtt2shutdown.path
      │
      ▼
 mqtt2shutdown.service
      │
      ▼
 shutdown-handler.sh
      │
      ▼
 Linux shutdown
```

The container writes a request file inside a shared directory.

A systemd `.path` unit monitors this directory and triggers a `.service` unit when a request is detected.

The service executes a privileged script responsible for performing the shutdown sequence.

---

## MQTT Topics

Example for `DEVICE_ID=FTP_SERVER`

### Commands

```text
mqtt2shutdown/FTP_SERVER/cmd/shutdown
```

### Telemetry

```text
mqtt2shutdown/FTP_SERVER/telemetry/availability
mqtt2shutdown/FTP_SERVER/telemetry/heartbeat
mqtt2shutdown/FTP_SERVER/telemetry/uptime
```

### Events

```text
mqtt2shutdown/FTP_SERVER/event/state
mqtt2shutdown/FTP_SERVER/event/event
mqtt2shutdown/FTP_SERVER/event/error
```

---

## Home Assistant Discovery

The application automatically publishes a Home Assistant Device Discovery payload.

Currently exposed entities:

* Connectivity binary sensor
* State sensor
* Event sensor
* Heartbeat sensor
* Error sensor
* Uptime sensor
* Shutdown button

---

## Docker Usage

Build image:

```bash
docker build . -t mqtt2shutdown
```

---

## Host Configuration

Create shared directory:

```bash
sudo mkdir -p /opt/mqtt2shutdown/commands

sudo chown root:root /opt/mqtt2shutdown
sudo chmod 755 /opt/mqtt2shutdown

sudo chown root:root /opt/mqtt2shutdown/commands
sudo chmod 777 /opt/mqtt2shutdown/commands
```

Define env variables:

```
sudo cp mqtt2shutdown.env /etc/mqtt2shutdown.env
chmod 600 /etc/mqtt2shutdown.env
```

This file contain specifics variables. Each user have to edit it.

```
sudo vim /etc/mqtt2shutdown.env
```

---

## Install Shutdown Handler

```bash
sudo cp shutdown-handler.sh /usr/local/bin/mqtt2shutdown-handler.sh

sudo chown root:root /usr/local/bin/mqtt2shutdown-handler.sh
sudo chmod 700 /usr/local/bin/mqtt2shutdown-handler.sh
```

---

## Install systemd Units

```bash
sudo cp systemd/* /etc/systemd/system/

sudo chmod 644 /etc/systemd/system/mqtt2shutdown*
sudo systemctl daemon-reload
```

Enable services:

```bash
sudo systemctl enable mqtt2shutdown-container.service
sudo systemctl enable mqtt2shutdown.path

sudo systemctl start mqtt2shutdown-container.service
sudo systemctl start mqtt2shutdown.path
```

---

## Security Model

The Docker container does not execute privileged commands.

The container only creates request files inside a shared directory.

Systemd is responsible for executing privileged operations on the host.

This design avoids:

* privileged containers
* Docker socket access
* direct execution of shutdown commands from MQTT

---

## Roadmap

Planned features:

* TLS support
* Command acknowledgement
* Command timestamp validation
* Replay protection
* Reboot support
* Wake-on-LAN support
* Dynamic capabilities
* Additional Home Assistant entities
* Improved error reporting

---

## Disclaimer

This software can remotely power off a machine.

Use at your own risk and test carefully before deploying on production systems.
