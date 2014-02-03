Alias /favicon.ico /home/matt/Kno/static/favicon.ico

Alias /static/ /home/matt/Kno/static/

<Directory /home/matt/Kno/static>
Order deny,allow
Allow from all
</Directory>

WSGIScriptAlias / /home/matt/Kno/kno/kno.wsgi

<Directory /usr/local/wsgi/scripts>
Order allow,deny
Allow from all
</Directory>
