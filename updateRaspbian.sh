#!/bin/bash 
echo "Se va a actualizar Raspbian..."
sleep 3
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y python-tk python-tk-dbg
sleep 3