#!/bin/bash 
echo "Se eliminara la versión instalada de Educascope..."
sleep 3
sudo rm -rfv /home/pi/educascopeApp
sudo rm -f /home/pi/Desktop/educascope.desktop /home/pi/Desktop/galeria-fotos.desktop /home/pi/Desktop/galeria-videos.desktop
echo "Se ha eliminado correctamente"
sleep 3