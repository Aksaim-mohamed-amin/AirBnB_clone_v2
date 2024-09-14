#!/usr/bin/env bash
# sets up web servers for the deployment of web_static

# Install nginx
sudo apt update
sudo apt install -y nginx

# Start nginx server
sudo service nginx start

# Create necessary folders
sudo mkdir -p /data/web_static/shared/ /data/web_static/releases/test/

# Create a fake html page
sudo touch /data/web_static/releases/test/index.html
sudo bash -c 'cat <<EOF > /data/web_static/releases/test/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AirBnB Clone</title>
</head>
<body>
    <h1>Hello World!</h1>
</body>
</html>
EOF'

# Create a symbolic link for test folder to current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -Rh ubuntu:ubuntu /data/

# Update Nginx configuration to serve content from /data/web_static/current/ to hbnb_static
sudo bash -c 'cat <<EOF > /etc/nginx/sites-available/default
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    # Add header to show which server handled the request
    add_header X-Served-By $HOSTNAME;

    # Document root
    root /var/www/html;
    index index.html;

    # Server name(s)
    server_name aksaim.tech www.aksaim.tech _;

    # Main location block for default handling
    location / {
        try_files $uri $uri/ =404;
    }

    # Location for serving static files from the hbnb project
    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }
}
EOF'

# Restart Nginx to apply the changes
sudo service nginx restart

# Ensure the script exits successfully
exit 0
