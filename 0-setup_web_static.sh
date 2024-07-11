#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

# Inctall Nginx
sudo apt update
sudo apt install -y nginx

# Create the necessary folders
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo -e '
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Hello World!</h1>
</body>
</html>' | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sfn /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu /data/
chgrp -R ubuntu /data/

# Update the nginx config file
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

# Restart nginx
sudo service nginx restart
