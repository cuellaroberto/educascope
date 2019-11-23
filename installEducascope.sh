#!/bin/bash 
current_dir="$(pwd)/educascopeApp" 
sudo cp -avr $current_dir /home/pi/
dir="$(pwd)/link/educascope.desktop" 
sudo cp -avr $dir /home/pi/Desktop/  
dir2="$(pwd)/link/galeria-fotos.desktop" 
sudo cp -avr $dir2 /home/pi/Desktop/ 
dir3="$(pwd)/link/galeria-videos.desktop" 
sudo cp -avr $dir3 /home/pi/Desktop/ 
echo "Educascope esta listo para usar.."
sleep 5
