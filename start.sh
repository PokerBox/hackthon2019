#!/bin/sh
echo Starting detect.py...

# Set the necessary environment variables - UBUNTU/UNITY/GNOME:
# export DISPLAY=$(w $(id -un) | awk 'NF > 7 && $2 ~ /tty[0-9]+/ {print $3; exit}')
export DISPLAY=0
export XDG_RUNTIME_DIR=/run/user/1000 
# export XAUTHORITY=/home/user/.Xauthority
# export GNOME_DESKTOP_SESSION_ID=true
# export DBUS_SESSION_BUS_ADDRESS=$(sed -zne 's/^DBUS_SESSION_BUS_ADDRESS=//p' /proc/`pgrep gnome-session -U $(id -u)`/environ)

#Open new terminal and execute the script:
# weston #&& /usr/bin/weston-terminal --fullscreen && sh cd /home/mendel/OSU-RM-tpu && python3 detect.py
cd /home/mendel/OSU-RM-tpu && python3 detect.py
