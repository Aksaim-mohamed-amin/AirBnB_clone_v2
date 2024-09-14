#!/usr/bin/bash

# Stop the Nginx service
echo "Stopping Nginx service..."
sudo service nginx stop

# Uninstall Nginx and remove its configurations
echo "Uninstalling Nginx..."
sudo apt-get remove --purge nginx nginx-common nginx-full -y

# Remove Nginx directories and configuration files
echo "Removing Nginx directories and configuration files..."
sudo rm -rf /etc/nginx
sudo rm -rf /var/www/html
sudo rm -rf /var/log/nginx
sudo rm -rf /var/cache/nginx

# Clean up unused dependencies and cache
echo "Cleaning up dependencies..."
sudo apt-get autoremove -y
sudo apt-get autoclean

# Verify Nginx removal
if ! command -v nginx &> /dev/null
then
    echo "Nginx has been successfully removed."
else
    echo "Error: Nginx is still installed."
fi

sudo rm -r /data 0-setup_web_static.sh
