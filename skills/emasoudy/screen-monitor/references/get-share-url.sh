#!/bin/bash
# Permanent Port for Screen Monitor Backend
PORT=18795
LAN_IP=$(ip route get 1 | awk '{print $7; exit}' 2>/dev/null || hostname -I | awk '{print $1}' || echo "localhost")
echo "http://${LAN_IP}:${PORT}/screen-share"
