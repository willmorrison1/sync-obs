#!/bin/bash

sudo echo "
[Unit]
Description=sync_obs Service
After=multi-user.target
[Service]
Type=idle
User=pi
RestartSec=10
WorkingDirectory=${BASE_DIR}/ircam/sync-obs
ExecStart=/usr/bin/python3 ${BASE_DIR}/ircam/sync-obs/sync.py --config_file ${BASE_DIR}/ircam/sync_config.json
Restart=always
[Install]
WantedBy=multi-user.target
" >  /etc/systemd/system/sync_obs.service

sudo chmod 644 /etc/systemd/system/sync_obs.service
sudo systemctl daemon-reload
sudo systemctl enable sync_obs.service
sudo systemctl daemon-reload
sudo systemctl start sync_obs.service