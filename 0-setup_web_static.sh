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

    # Document root
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    # Server name(s)
    server_name _;

    # Add header to show which server handled the request
    add_header X-Served-By \$hostname;

    # Main location block for default handling
    location / {
		try_files \$uri \$uri/ =404;
    }

    # Location for serving static files from the hbnb project
    location /hbnb_static {
		alias /data/web_static/current/;
    }
}
EOF'

# Update the home page to return the custom message
sudo bash -c 'cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to My World!</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f8ff;
            color: #333;
            text-align: center;
            margin-top: 50px;
        }
        h1 {
            color: #4CAF50;
        }
        p {
            font-size: 18px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            border: 2px solid #4CAF50;
            border-radius: 10px;
            background-color: #fff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>&#127881; Hello there!</h1>
        <p>I&apos;m Amin, and you&apos;ve stumbled upon my little corner of the internet. &#127760;</p>
        <p>Get ready for something amazing—it&apos;s coming soon, and it&apos;s going to be epic! &#128640;</p>
        <p>Stay tuned and have a great day! &#128578;</p>
    </div>
</body>
</html>
EOF'

# Restart Nginx to apply the changes
sudo service nginx restart

# Ensure the script exits successfully
exit 0
