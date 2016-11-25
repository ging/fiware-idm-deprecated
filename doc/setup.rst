***********************
Production Set Up Guide
***********************

.. contents::
   :local:
   :depth: 3

.. _production-guide:

This section covers how to set up the IdM for production, covering
topics like email sending, No CAPTCHA reCAPTCHA support or how to serve
static and media files. Some topics, for example HTTPS, are beyond the
scope of this documentation and only some pointers to related
documentation are provided as a starting point.

Make sure to also check the documentation for the respective parts of the IdM
for more in-depth information of the components.

- Back-end `ging/keystone <https:/github.com/ging/keystone>`__

- Front-end `ging/horizon <https:/github.com/ging/horizon>`__

MySQL
=====

If you have installed the IdM using the automated tools the back-end
(Keystone) will be configured to use a SQLite database. This is NOT
recommended for production, we strongly advise to switch to a
production-ready SQL database. This guide covers how to configure MySQL
but any other database compatible with
`SQLAlchemy <http://www.sqlalchemy.org/>`__ would probably work too.

Install MySQL
-------------

::

    sudo apt-get install mysql-server

Configure Keystone
------------------

Edit **keystone/etc/keystone/keystone.conf** and change the [database]
section.

::

    [database]  
    # The SQLAlchemy connection string used to connect to the database  
    connection = mysql://keystone:KEYSTONE_DBPASS@MYSQL_ADDRESS/keystone  

Use the password that you set previously to log in as root. Create a
keystone database user:

::

    # mysql -u root -p  
    mysql> CREATE DATABASE keystone;  
    mysql> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'KEYSTONE_DBPASS';     
    mysql> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'KEYSTONE_DBPASS';  

Populate Database
-----------------

You need to create the database tables and populate them.

.. include:: introduction.rst
  :start-after: begin-database
  :end-before: end-database


You can find aditional help for setting up Keystone + MySQL
`here <http://docs.openstack.org/juno/install-guide/install/apt/content/keystone-install.html>`__.


.. _production-apache:


Web Server (Apache + mod_wsgi)
===============================

The web server used by the tools is a development server that should NOT
be used for a production setting. There are several servers and
configurations to serve a Django (Python) web application but only
Apache + mod_wsgi will be covered here. Take a look at the `oficial
Django
documentation <https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/>`__
for other options available and further information on this topic.

Install apache and mod_wsgi
----------------------------

::

    sudo apt-get install apache2 libapache2-mod-wsgi

Configure Apache
----------------

The details on how to correctly configure Apache or
set up HTTPS are beyond the scope this document, check the `Django
documentation <https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/modwsgi/>`__
and `Apache HTTPS
documentation <http://httpd.apache.org/docs/2.4/ssl/ssl_howto.html>`__
for a starting point. Make sure that the following elements are present:
(take special care with the
`venv <https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/modwsgi/#using-a-virtualenv>`__)

.. code-block:: apacheconf

    WSGIPassAuthorization On  
    WSGIScriptAlias / [PATH_TO_HORIZON]/horizon/openstack_dashboard/wsgi/django.wsgi
    WSGIPythonPath [PATH_TO_HORIZON]/horizon/openstack_dashboard:[PATH_TO_HORIZON]/horizon/.venv/lib/python2.7/site-packages

If you want to serve your static and media files from Apache itself,
also make sure to create the Alias

.. code-block:: apacheconf

    Alias /media/ /root/horizon/media/
    Alias /static/ /root/horizon/static/
    Alias /assets/ /root/horizon/static/fiware/
    <Directory [PATH_TO_HORIZON]/horizon/static>
      Require all granted
    </Directory>
    <Directory [PATH_TO_HORIZON]/horizon/media>
      Require all granted
    </Directory>

As reference, here you can see a full Apache configuration file using HTTPS

.. code-block:: apacheconf

    <IfModule mod_ssl.c>
    <VirtualHost *:443>
        ServerName  foo
        ServerAdmin bar

        WSGIScriptAlias / /home/someone/horizon/openstack_dashboard/wsgi/django.wsgi

        <Directory /home/someone/horizon/openstack_dashboard/wsgi>
          Order allow,deny
          Allow from all
        </Directory>

        Alias /media/ /home/someone/horizon/media/
        Alias /static/dashboard/fonts /home/someone/horizon/openstack_dashboard/static/dashboard/fonts
        Alias /static/dashboard/img /home/someone/horizon/openstack_dashboard/static/dashboard/img
        Alias /static/dashboard/css /home/someone/horizon/static/dashboard/css
        Alias /static/dashboard/js /home/someone/horizon/static/dashboard/js

        <Directory /path/to/foo/static>
         Require all granted
        </Directory>

        <Directory /path/to/foo/media>
         Require all granted
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/error.log

        # Possible values include: debug, info, notice, warn, error, crit,
        # alert, emerg.
        LogLevel debug

        CustomLog ${APACHE_LOG_DIR}/ssl_access.log combined

        #   SSL Engine Switch:
        #   Enable/Disable SSL for this virtual host.
        SSLEngine on

        SSLCertificateFile    /etc/ssl/private/someplace.org/somecert.crt
        SSLCertificateKeyFile /etc/ssl/private/someplace.org/*.somepem.pem 
        SSLCertificateChainFile    /etc/ssl/private/someplace.org/chain.crt

        <FilesMatch "\.(cgi|shtml|phtml|php)$">
            SSLOptions +StdEnvVars
        </FilesMatch>
        <Directory /usr/lib/cgi-bin>
            SSLOptions +StdEnvVars
        </Directory>

        BrowserMatch "MSIE [2-6]" \
            nokeepalive ssl-unclean-shutdown \
            downgrade-1.0 force-response-1.0
        # MSIE 7 and newer should be able to use keepalive
        BrowserMatch "MSIE [17-9]" ssl-unclean-shutdown

    </VirtualHost>
    </IfModule>

    #rdeirection to the secure version
    <VirtualHost 0.0.0.0:80>
        ServerName foo2
        Redirect permanent / foo
    </VirtualHost>



Collect Static Assets
---------------------

Now, go to the folder you have installed Horizon and run

::

    sudo tools/with_venv.sh python manage.py collectstatic
    sudo tools/with_venv.sh python manage.py compress --force

Edit the ``local_settings.py`` file and set

::

    DEBUG = False
    ALLOWED_HOSTS = [
        'your.domain.com',
        'another.domain.es'
    ]
    SECRET_KEY = 'arandomstringhere' # DON'T LEAVE THIS SAMPLE STRING

.. warning:: Please set your ``SECRET_KEY``. A known SECRET_KEY is a huge security vulnerability.
More information `here <https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-SECRET_KEY>`__

NO CAPTCHA reCAPTCHA
====================

.. begin-captcha

.. warning:: Don't deploy KeyRock in a public domain with CAPTCHA disabled.

Get your keys
`here <https://www.google.com/recaptcha/admin#createsite>`__. More
documentation in `the captcha package
repository <https://github.com/ImaginaryLandscape/django-nocaptcha-recaptcha>`__.

.. code-block:: python

    USE_CAPTCHA = False
    NORECAPTCHA_SITE_KEY   = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
    NORECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

.. end-captcha

.. _production-email:

Email Configuration
===================

The IdM can't send emails by itself, you must set up a SMTP server to
send it. This section covers how to set up a mail server using
`POSTFIX <http://www.postfix.org/>`__ and connect the front-end to it.
Further information can be found in the `Django
documentation <https://docs.djangoproject.com/en/1.8/topics/email/#email-backends>`__.

Install and configure `POSTFIX <http://www.postfix.org/>`__, 
`Ubuntu guide <https://help.ubuntu.com/lts/serverguide/postfix.html>`__.

::

    sudo apt-get install postfix

Go to the folder where you have installed the front-end and edit
local_settings.py

::

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

This will get the settings from the default SMTP server in your host (it
should be POSTFIX after installing it) If you are not running POSTFIX in
the same host or want to use a different configuration, make use of the
following settings

::

    # Configure these for your outgoing email host
    EMAIL_HOST = 'smtp.my-company.com'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = 'djangomail'
    EMAIL_HOST_PASSWORD = 'top-secret!'
    EMAIL_URL = 'your-webstie-domain.com'
    DEFAULT_FROM_EMAIL = 'your-no-reply-address'
    EMAIL_SUBJECT_PREFIX = '[Prefix for emails subject]'
