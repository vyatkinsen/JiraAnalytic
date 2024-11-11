#!/bin/sh
sudo apt update
sudo apt install python3.12-venv python3.12-dev python3-pip
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python setup.py install