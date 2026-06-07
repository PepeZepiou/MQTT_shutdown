#!/bin/bash

rm -f /opt/mqtt2shutdown/commands/shutdown.request

systemctl poweroff
