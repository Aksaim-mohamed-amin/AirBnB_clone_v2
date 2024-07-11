#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

# Inctall Nginx
sudo apt update
sudo apt install -y nginx


# Create necessary folders and set permissions
sudo mkdir -p /data/web_static/{shared,releases/test}
sudo ln -sfn /data/web_static/releases/test /data/web_static/current
sudo chown -R ubuntu:ubuntu /data

# Create index.html
index='<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Under Construction</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
        h1 {
            color: #333;
        }
        p {
            color: #666;
        }
        footer {
            margin-top: 50px;
            font-style: italic;
            color: #999;
        }
    </style>
</head>
<body>
    <h1>Under Construction</h1>
    <p>The site is under construction.</p>
    <p>Thank you for your visit!</p>
    <footer>Aksaim Mohamed Amin</footer>
</body>
</html>'

sudo bash -c "cat <<EOF > /data/web_static/releases/test/index.html
$index
EOF"

# Updte Nginx config
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
       location /hbnb_static {
                alias /data/web_static/current/;
       }
}
EOF'

# Restart Nginx
sudo service nginx restart
