#!/bin/sh

apt update && apt -y upgrade
apt install -y python3-pip
pip3 install -r requirements.txt
