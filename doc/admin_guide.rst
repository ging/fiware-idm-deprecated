*************************************
Installation and Administration Guide
*************************************

.. contents::
   :local:
   :depth: 3

Introduction
============

Welcome to the Installation and Administration Guide for the Identity
Management - KeyRock Generic Enabler. This section will cover how to
install, configure and administrate a working instance of KeyRock. 

If you want to deploy it in a production environment, take a look at 
the :ref:`Production set up Guide <production-guide>`.

.. include:: introduction.rst
  :start-after: begin-requirements
  :end-before: end-requirements


.. _step-installation:

Step by Step Installation
=========================

The IdM is composed of two separated services, that interact with each other. The web portal is
based on OpenStack's Dashboard, Horizon. The back-end is a REST service based on OpenStack's Identity 
Provider, Keystone. 

They can be installed both on the same machine (or docker container) or in separated ones. If separated
machines is the preferred option, make sure there is connectivity between them, as Horizon needs to be
able to consume Keystone's REST API.

.. note:: 

  To be able to log into the IdM, you will need a working
  Keystone backend. Please complete all the steps in this page in order to
  have a complete and working IdM.

Installing Horizon
------------------


1. Installation
^^^^^^^^^^^^^^^

.. include:: introduction.rst
  :start-after: begin-horizon-installation
  :end-before: end-horizon-installation

.. _horizon-configuration:

2. Configuration
^^^^^^^^^^^^^^^^

To configure Horizon, the configuration file can be found in
``openstack_dashboard/local/local_settings.py``. This file holds
sensible defaults for a common installation but you might need to tweek
them to fit your use case.

If you are running Keystone on your own machine the address will be
``http://localhost:5000/v3``. If Keystone is configured to run on a
different port and/or address you should set this accordingly.

.. code-block:: python

    OPENSTACK_HOST = "Keystone server IP address"
    OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3" % OPENSTACK_HOST

Email
'''''

Configure this for your outgoing email host or leave the default values for the console email backend. More details on how to configure this can be found `in the Django docs <https://docs.djangoproject.com/en/1.8/topics/email/>`__ and in the :ref:`Production Set up Guide <production-email>`.

Keystone Account for the IdM to perform tasks like user registration
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code-block:: python

    OPENTACK_KEYSTONE_ADMIN_CREDENTIALS = {
     'USERNAME': 'the_username',
     'PASSWORD': 'the_password',
     'PROJECT': 'the_projectname',
    }

User Registration settings
''''''''''''''''''''''''''

This setting enables email domain
filtering on user registration. Set to 'whitelist', 'blacklist' or
comment it out for no filtering.

.. code-block:: python

    EMAIL_LIST_TYPE = 'blacklist'

More info :ref:`here <email-lists>`.

noCAPTCHA reCAPTCHA
'''''''''''''''''''

.. note:: If you want to disable the captcha, set ``USE_CAPTCHA`` to ``False``.

.. include:: setup.rst
  :start-after: begin-captcha
  :end-before: end-captcha

FIWARE Applications and Roles
'''''''''''''''''''''''''''''

These settings map applications used
in the FIWARE-Lab environment and are needed for automated tasks, for
example granting the **Purchaser** role in the **Store** to any
created organization. Depending on your use case you might need or
want to modifiy them, but normal installations in a *fiware-like*
environment won't need to change the following code. Keep in mind
that if your use case differs too much you might need to change the
code to prevent some of these operations. If you are not using the
scripts you will need to check the ids in through the API or in the
database yourself.

.. code-block:: python

    FIWARE_PURCHASER_ROLE_ID = 'id'
    FIWARE_PROVIDER_ROLE_ID = 'id'
    FIWARE_IDM_ADMIN_APP = 'idm'
    FIWARE_CLOUD_APP = 'Cloud'
    FIWARE_DEFAULT_CLOUD_ROLE_ID = 'id'
    FIWARE_DEFAULT_APPS = [
     'Store',
    ]

Keystone roles
''''''''''''''

These settings map to normal Keystone roles that are
used by the IdM. As with the FIWARE Applications and Roles settings,
they depend on your use case and , if you are not using the
installation scripts, you will have to create them yourself.

.. code-block:: python

    KEYSTONE_OWNER_ROLE = 'owner'
    KEYSTONE_TRIAL_ROLE = 'trial'
    KEYSTONE_BASIC_ROLE = 'basic'
    KEYSTONE_COMMUNITY_ROLE = 'community'
    MAX_TRIAL_USERS = 100
    OPENSTACK_KEYSTONE_ADMIN_ROLES = [
    KEYSTONE_OWNER_ROLE,
     'admin',
    ]
    

AuthZForce GE Configuration
'''''''''''''''''''''''''''

These settings configure the connection to an `Authorization PDP GE <http://catalogue.fiware.org/enablers/authorization-pdp-authzforce/>`__  instance to create permmisions to your applications. If the AZF instance is secured by a `PEP Proxy GE <http://catalogue.fiware.org/enablers/pep-proxy-wilma>`__ you can also set a magic key to bypass the policy enforcement point. 

.. code-block:: python

    # ACCESS CONTROL GE
    ACCESS_CONTROL_URL = 'http://azf_host:6019'
    ACCESS_CONTROL_MAGIC_KEY = 'azf_pep_key'
    
Endpoints Management Dashboard
''''''''''''''''''''''''''''''

This admin-only dashboard requires some settings before it can be used. The Keystone project to which all services accounts are given admin permissions must be provided in the ``SERVICE_PROJECT`` setting. The ``AVAILABLE_SERVICES`` setting contains the set of services whose endpoints can be managed from the Dashboard. Both ``type`` and ``description`` are mandatory, while the ``extra_roles`` setting is optional and has to do with special roles being assigned to the given service account, either in a domain or in a project.

.. code-block:: python

    # ENDPOINTS MANAGEMENT DASHBOARD
    SERVICE_PROJECT = 'service'
    AVAILABLE_SERVICES = {
      'swift': {'type': 'Object storage',
                'description': 'Stores and retrieves arbitrary unstructured data objects via a RESTful, HTTP based API. \
                                It is highly fault tolerant with its data replication and scale out architecture. Its \
                                implementation is not like a file server with mountable directories.'},
      'nova': {'type': 'Compute',
               'description': 'Manages the lifecycle of compute instances in an OpenStack environment. Responsibilities \
                               include spawning, scheduling and decomissioning of machines on demand.'},
      'cinder': {'type': 'Block storage',
                 'description': 'Provides persistent block storage to running instances. Its pluggable driver architecture \
                                 facilitates the creation and management of block storage devices.',
                 'extra_roles': [{'role': 'cinder-role', 'domain': 'cinder-domain'}]
                },
    }

3. Django settings
^^^^^^^^^^^^^^^^^^

The settings for all the Django configuration are located at
``horizon/openstack_dashboard/settings.py``

Here we added some django apps, middleware, etc. You can check the file
for reference but there is no extra configuration needed here.

4. Running a development server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run a simple server to try out and check the IdM installation or for
developping purpuses you can use Django's development server that comes
with the IdM installation, which will automatically run in port 8000:

  $ sudo tools/with_venv.sh python manage.py runserver

You can also explicitly run:::

  $ sudo tools/with_venv.sh python manage.py runserver IP:PORT

For more documentation about this server, head on to `django
docs <https://docs.djangoproject.com/en/1.7/ref/django-admin/#django-admin-runserver>`__

.. warning:: 
  As the Django documentation states: DO NOT USE THIS
  SERVER IN A PRODUCTION SETTING. It has not gone through security audits
  or performance tests. For a production setting, follow the :ref:`Production Set up Guide <production-apache>`.

Installing Keystone
-------------------

1. Installation
^^^^^^^^^^^^^^^

.. include:: introduction.rst
  :start-after: begin-keystone-installation
  :end-before: end-keystone-installation


.. _keystone-configuration:

2. Configuration
^^^^^^^^^^^^^^^^

After creating the default configuration file, the following lines must
be uncommented and set to your custom values.

.. code-block:: python

     admin_token=ADMIN
     admin_port=35357
     public_port=5000


3. Run Keystone
^^^^^^^^^^^^^^^

To run Keystone, we must either run it as a service or in a console with
the following command::

  $ sudo tools/with_venv.sh bin/keystone-all -v


.. _keystone-as-service:

4. Configuring Keystone as a service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to ad the Keystone to init.d to run it as a service there
are serveral possibilities. You can try to reuse the scripts provided
with Keystone or you can add a *.conf* file to ``etc/init``. Here is a
basic example:

Create the following file at: ``/etc/init/keystone_idm.conf``

.. code-block:: bash

    # keystone_idm - keystone_idm job file
     description "Service conf file for the IdM backend based in Keystone"
     author "Enrique Garcia Navalon <garcianavalon@gmail.com>"
     start on (local-filesystems and net-device-up IFACE!=lo)
     stop on runlevel [016]
    # Automatically restart process if crashed
    respawn
    setuid root
    script
    cd $absolute_keystone_path
    #activate the venv
    . .venv/bin/activate
    #run keystone
    bin/keystone-all
    end script

To run Keystone, you can now run it with the following command::

  $ sudo service keystone_idm start

5. Running tests
^^^^^^^^^^^^^^^^

In order to test, we use the Keystone built in system: **tox** and
**testr**.

To execute all tests::

  $ sudo tox

To Execute the extension tests (in this case for oauth2)::

  $ sudo tox -e py27 -- keystone.tests.test_v3_oauth2

.. note::
  To debug during test, add the following parameter to the command: ``-e debug``

System Administration
=====================

.. _cli-tools:

CLI tools
---------

A set of commands is provided to help with some common tasks like updating endpoints and regions, a console to execute python against Keystone API, etc.

To install them

::

  $ git clone https://github.com/ging/fiware-idm imd-admin && cd imd-admin
  $ sudo pip install -r requirements.txt
  $ sudo python setup.py install


Get to know how to use them and the available commands by using the following

::
  
  $ idm-admin --help


.. _email-lists:

White and black lists
---------------------

As administrator of IdM KeyRock you can manage white and black lists in
order to allow and deny access to users by their email domains.

There is a file for each of the list which you can find at
``/horizon/openstack_dashboard/fiware_auth/blacklist.txt`` or
``whitelist.txt``.

-  `Whitelist`: add a line for each of the domains that are allowed. No other domain will be allowed to register users.

-  `Blacklist`: add a line for each of the domains that are not allowed. If a user has an email from this domain, they will not be able to register.

Sanity Check Procedures
=======================

The Sanity Check Procedures are the steps that a System Administrator
will take to verify that an installation is ready to be tested. This is
therefore a preliminary set of tests to ensure that obvious or basic
malfunctioning is fixed before proceeding to unit tests, integration
tests and user validation.

End to End testing
-------------------

1. Verify that the host address of IdM can be reached. By default, web
   access will show a Login Page.

2. Acquire a valid username and password and access with those
   credentials. The resulting web page is the landing page of the IdM
   KeyRock Portal.

3. Verify that you can view the list of applications, organizations,
   etc.

List of Running Processes
-------------------------

In you have run the Horizon and Keystone run commands without errors,
the portal is up and running.

Network interfaces Up & Open
----------------------------

-  TCP port 80 should be accessible to the web browsers in order to load
   the IdM Portal (8000 for development).
-  Ports 5000 and 35357 are Keystone's public and admin port
   respectively.

Databases
=========

If you have correctly populated the database when installing the GE, the
connection with it is up and running.

The databases and tables needed are::

     +--------------------------------------+
     | Tables_in_keystone                   |
     +--------------------------------------+
     | access_token_oauth2                  |
     | assignment                           |
     | authorization_code_oauth2            |
     | consumer_credentials_oauth2          |
     | consumer_oauth2                      |
     | credential                           |
     | domain                               |
     | endpoint                             |
     | endpoint_group                       |
     | group                                |
     | id_mapping                           |
     | migrate_version                      |
     | permission_fiware                    |
     | policy                               |
     | project                              |
     | project_endpoint                     |
     | project_endpoint_group               |
     | region                               |
     | revocation_event                     |
     | role                                 |
     | role_fiware                          |
     | role_organization_fiware             |
     | role_permission_fiware               |
     | role_user_fiware                     |
     | service                              |
     | token                                |
     | trust                                |
     | trust_role                           |
     | user                                 |
     | user_group_membership                |
     | user_registration_activation_profile |
     | user_registration_reset_profile      |
     +--------------------------------------+

Diagnosis Procedures
====================

The Diagnosis Procedures are the first steps that a System Administrator
will take to locate the source of an error in a GE. Once the nature of
the error is identified with these tests, the system admin will very
often have to resort to more concrete and specific testing to pinpoint
the exact point of error and a possible solution. Such specific testing
is out of the scope of this section.

Resource availability
---------------------

-  Verify that 2.5MB of disk space is left using the UNIX command 'df'

Remote Service Access
---------------------

Please make sure port 80 is accessible (port 8000 in development mode).

Resource consumption
--------------------

Typical memory consumption is 100MB and it consumes almost the 1% of a
CPU core of 2GHz, but it depends on user demand.

I/O flows
---------

Clients access the KeyRock Interface through the client's Web Browser.
This is simple HTTP traffic. It makes requests to the local database.
