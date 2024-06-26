#!/usr/bin/env bash
# Script that configures web servers for deployment

if [[ $EUID -ne 0 ]]; then
    echo "You need to be root"
    exit 1
fi

# Check if nginx is available before installing nginx
command -v nginx > /dev/null
if [[ $? -eq 1 ]]; then
    apt install nginx -y
fi

# Create the required directories
mkdir -p /data/web_static/shared 2> /dev/null
mkdir -p /data/web_static/releases/test 2> /dev/null

# Dummy HTML used for test
echo "
<html lang='en'>
    <head>
        <title>Airbnb Clone</title>
        <style>
        .container {
            margin: 0 auto;
        }

        .text {
            font-size: 2em;
            text-align: center;
        }

        hr {
            border: 2px solid black;
        }
        </style>
    </head>
    <body>
        <div class='container'>
            <h1 class='text'>Yep, it works. I am $HOSTNAME</h1>
            <hr>
        </div>
    </body>
</html>
" > /data/web_static/releases/test/index.html

# Create symbolic link for current release
ln -sf /data/web_static/releases/test /data/web_static/current

# Grant user permissions over directories
chown -R ubuntu:ubuntu /data

# Update nginx configuration to add alias configuration
grep -q "location /hbnb_static {" /etc/nginx/sites-available/default
if [[ $? -eq 1 ]]; then
    sed -i "/server_name _;/a \\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}" /etc/nginx/sites-available/default
fi

# Restart nginx
service nginx restart
