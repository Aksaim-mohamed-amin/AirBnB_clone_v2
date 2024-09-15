# Setup a new server for deployment

$nginx_conf = "
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    # Document root
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    # Server name(s)
    server_name _;

    # Add header to show which server handled the request
    add_header X-Served-By ${hostname};

    # Main location block for default handling
    location / {
		try_files $uri $uri/ =404;
    }

    # Location for serving static files from the hbnb project
    location /hbnb_static {
		alias /data/web_static/current/;
    }
}
"

$html_page = '
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
'

package { 'nginx':
  ensure   => 'present',
  provider => 'apt'
}

-> file { '/data':
  ensure  => 'directory'
}

-> file { '/data/web_static':
  ensure => 'directory'
}

-> file { '/data/web_static/releases':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test':
  ensure => 'directory'
}

-> file { '/data/web_static/shared':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => $html_page,
}

-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
}

-> exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $nginx_conf
}

-> exec { 'nginx restart':
  path => '/etc/init.d/'
}
