Production Set Up Guide
=================

This section covers how to set up the IdM for production, covering topics like email sending, No CAPTCHA reCAPTCHA support or how to serve static and media files. Some topics, for example HTTPS, are beyond the scope of this documentation and only some pointers to related documentation are provided as a starting point.

Make sure to also check the wikis for the respective parts of the IdM for more in-depth information of the components.

Back-end [ging/keystone](https:/github.com/ging/keystone)  

Front-end [ging/horizon](https:/github.com/ging/horizon)  

### MySQL

If you have installed the IdM using the automated tools the back-end (Keystone) will be configured to use a SQLite database. This is NOT recommended for production, we strongly advise to switch to a production-ready SQL database. This guide covers how to configure MySQL but any other database compatible with [SQLAlchemy](http://www.sqlalchemy.org/) would probably work too.

Install MySQL
```
sudo apt-get install mysql-server
```

Edit keystone/etc/keystone/keystone.conf and change the [database] section.
```
[database]  
# The SQLAlchemy connection string used to connect to the database  
connection = mysql://keystone:KEYSTONE_DBPASS@MYSQL_ADDRESS/keystone  
```

Use the password that you set previously to log in as root. Create a keystone database user:
```
# mysql -u root -p  
mysql> CREATE DATABASE keystone;  
mysql> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'KEYSTONE_DBPASS';     
mysql> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'KEYSTONE_DBPASS';  
```

You need to create the database tables and populate them with the initial data. Run the following fabric tasks (remember to activate the virtual environment)
```
fab localhost keystone.database_create
fab localhost keystone.populate
```

You can find aditional help for setting up Keystone + MySQL [here](http://docs.openstack.org/havana/install-guide/install/apt/content/keystone-install.html).

### Web Server (Apache + mod_wsgi)
The web server used by the tools is a development server that should NOT be used for a production setting. There are several servers and configurations to serve a Django (Python) web application but only Apache + mod_wsgi will be covered here. Take a look at the [oficial Django documentation](https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/) for other options available and further information on this topic.

Install apache and mod_wsgi
```
sudo apt-get install apache2 libapache2-mod-wsgi
```
Configure Apache. The details on how to correctly configure Apache or set up HTTPS are beyond te scope this document, check the [Django documentation](https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/modwsgi/) and [Apache HTTPS documentation](http://httpd.apache.org/docs/2.4/ssl/ssl_howto.html) for a starting point. Make sure that the following elements are present: (take special care with the [venv](https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/modwsgi/#using-a-virtualenv))
```
WSGIPassAuthorization On  
WSGIScriptAlias / [PATH_TO_HORIZON]/horizon/openstack_dashboard/wsgi/django.wsgi
WSGIPythonPath [PATH_TO_HORIZON]/horizon/openstack_dashboard:[PATH_TO_HORIZON]/horizon/.venv/lib/python2.7/site-packages
```
If you want to serve your static and media files from Apache itself, also make sure to create the Alias
```
Alias /media/ /root/horizon/media/
Alias /static/ /root/horizon/static/
Alias /assets/ /root/horizon/static/fiware/
<Directory [PATH_TO_HORIZON]/horizon/static>
  Require all granted
</Directory>
<Directory [PATH_TO_HORIZON]/horizon/media>
  Require all granted
</Directory>
```

Now, go to the folder you have installed Horizon and run
```
sudo tools/with_venv.sh python manage.py collectstatic
sudo tools/with_venv.sh python manage.py compress --force
```
Edit the local_settings.py file and set
```
DEBUG = False
ALLOWED_HOSTS = [
    'your.domain.com',
    'another.domain.es'
]
SECRET_KEY = 'somethingsecret'
```

### NO CAPTCHA reCAPTCHA
You can find how to set up the reCAPTCHA field for user registration in the [installation and administration guide](doc/admin_guide.md)

### EMAIL
The IdM can't send emails by itself, you must set up a SMTP server to send it. This section covers how to set up a mail server using [POSTFIX](http://www.postfix.org/) and connect the front-end to it. Further information can be found in the [Django documentation](https://docs.djangoproject.com/en/1.8/topics/email/#email-backends).

Install and configure [POSTFIX](http://www.postfix.org/), [Ubuntu guide](https://help.ubuntu.com/lts/serverguide/postfix.html).
```
sudo apt-get install postfix
```
Go to the folder where you have installed the front-end and edit local_settings.py
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
This will get the settings from the default SMTP server in your host (it should be POSTFIX after installing it) If you are not running POSTFIX in the same host or want to use a different configuration, make use of the following settings
```
# Configure these for your outgoing email host
EMAIL_HOST = 'smtp.my-company.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'djangomail'
EMAIL_HOST_PASSWORD = 'top-secret!'
```