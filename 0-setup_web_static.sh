#!/usr/bin/bash
# sets up web servers for the deployment of web_static

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
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content from /data/web_static/current/ to hbnb_static
sudo bash -c 'cat <<EOF > /etc/nginx/sites-available/default
server {
       listen 80 default_server;
       listen [::]:80 default_server;

       root /var/www/html;
       index index.html;

       server_name _;

       location / {
       		try_files \$uri \$uri/ =404;
		add_header X-Served-By \$hostname;
       }

       location /hbnb_static/ {
       		alias /data/web_static/current/;
		index index.html;
       }
}
EOF'

# Restart Nginx to apply the changes
sudo service nginx restart

# Ensure the script exits successfully
exit 0
