#!/bin/sh
# Installs the attendance page as a service on this Linux machine (port 8207).
set -e
DIR=/opt/villa207
sudo mkdir -p $DIR && sudo cp -r ./* $DIR/
sudo tee /etc/systemd/system/villa207.service >/dev/null <<UNIT
[Unit]
Description=Villa 207 attendance page
After=network-online.target
[Service]
ExecStart=/usr/bin/python3 $DIR/server.py
Restart=always
[Install]
WantedBy=multi-user.target
UNIT
sudo systemctl daemon-reload && sudo systemctl enable --now villa207
sleep 2
echo "--- local test:"; curl -s -m 45 http://127.0.0.1:8207/relay.php?ping=1; echo
