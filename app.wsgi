<VirtualHost *:80>
    ServerName lukas.educationinportugal.com

    WSGIScriptAlias / /var/www/html/FlaskProject1/app.wsgi

    <Directory /var/www/html/FlaskProject1>
        Require all granted
    </Directory>

    Alias /static /var/www/html/FlaskProject1/static
    <Directory /var/www/html/FlaskProject1/static>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

import sys
import os

sys.path.insert(0, '/var/www/html/FlaskProject1')

from app import app as application
