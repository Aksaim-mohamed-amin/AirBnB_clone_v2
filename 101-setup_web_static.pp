# Install Nginx
package { 'nginx':
  ensure => installed,
}

# Create the necessary directories
file { '/data/web_static/shared/':
  ensure  => 'directory',
  recurse => true,
}

file { '/data/web_static/releases/test/':
  ensure  => 'directory',
}

# Create a fake HTML page
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '
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
</html>',
}

# Create a symbolic link for the test folder to current
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}

# Set ownership for /data/ folder
file { '/data':
  ensure  => 'directory',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => '
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
}',
  notify  => Service['nginx'],
}

# Manage Nginx service
service { 'nginx':
  ensure => 'running',
  enable => true,
}
