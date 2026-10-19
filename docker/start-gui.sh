#!/bin/sh
# 仮想ディスプレイ上で GUI を起動し、 noVNC (port 6080) でブラウザへ表示します。
set -eu

export DISPLAY=:99
Xvfb "$DISPLAY" -screen 0 300x300x24 -nolisten tcp &
while [ ! -e /tmp/.X11-unix/X99 ]; do sleep 0.1; done

x11vnc -display "$DISPLAY" -forever -shared -nopw -localhost -rfbport 5900 -quiet &
websockify --web /opt/novnc 6080 localhost:5900 &

exec python poke_shiny.py
