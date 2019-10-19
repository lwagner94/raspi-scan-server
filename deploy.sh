#!/bin/sh

scp files/scan.py root@192.168.0.4:/usr/local/bin/scan.py
ssh root@192.168.0.4 chmod +x /usr/local/bin/scan.py
