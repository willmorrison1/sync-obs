#!/bin/bash

sudo echo "
[Unit]
Description=sync_obs Service
After=multi-user.target
[Service]
Type=idle
User=smurobs
RestartSec=10
WorkingDirectory=/home/smurobs/sync-obs/
ExecStart=/usr/bin/python3 /home/smurobs/sync-obs/sync.py
Restart=always
[Install]
WantedBy=multi-user.target
" >  /etc/systemd/system/sync_obs.service

sudo chmod 644 /etc/systemd/system/sync_obs.service
sudo systemctl daemon-reload
sudo systemctl enable sync_obs.service
sudo systemctl daemon-reload
sudo systemctl start sync_obs.service