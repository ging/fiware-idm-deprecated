# Installation and Administration Guide

- [Introduction](#introduction)
    - [Requirements](#requirements)
- [System Installation](#system-installation)
    - [Installing Horizon](#installing-horizon)
    - [Installing Keystone](#installing-keystone)
- [System Administration](#system-administration)
    - [White and black lists](#white-and-black-lists)
- [Sanity Check Procedures](#sanity-check-procedures)
    - [End to End testing](#end-to-end-testing)
    - [List of Running Processes](#list-of-running-processes)
    - [Network interfaces Up & Open](#network-interfaces-up--open)
    - [Databases](#databases)
- [Diagnosis Procedures](#diagnosis-procedures)
    - [Resource availability](#resource-availability)
    - [Remote Service Access](#remote-service-access)
    - [Resource consumption](#resource-consumption)
    - [I/O flows](#io-flows)

## Introduction

Welcome to the Installation and Administration Guide for the Identity Management - KeyRock Generic Enabler. This generic enabler has been developed as an Open Source project, therefor this guide points to the appropriate online content that has been created for this it.

The recommended way of intalling the IdM is through the installation tools. You can find the documentation on how to use this tools [here](https://github.com/ging/fiware-idm#def-build). This guide will cover all the steps required to successfully install the IdM, in case you would rather install it step by step and as a reference of the installation scripts tasks.
 

### Requirements

This installation guide is made for the installation of Identity Management - KeyRock in a Ubuntu 12.04 (LTS) server.

Both Horizon, for the front-end, and Keystone, for the back-end, must be installed in order for the the generic enabler to run correctly.

## System Installation

### Installing Horizon

**Note:** To be able to log into the IdM, you will need a working Keystone backend. Please complete the steps in this page in order to have a complete and working IdM.

#### 1. Install Ubuntu dependencies and repository

Downloading the code and installing the dependencies will create a python virtual environment with all the libraries needed. To check for more details, the *requirement.txt* file has a list of all the libraries needed.

<pre>
 $ sudo apt-get update
 $ sudo apt-get install git python-dev python-virtualenv libssl-dev libffi-dev libjpeg8-dev
 $ git clone https://github.com/ging/horizon.git
 $ cd horizon
 $ sudo python tools/install_venv.py
</pre>

Create a basic configuration file:

<pre>
 $ cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py
</pre>

#### **2. Configuring Horizon**

To configure Horizon, the configuration file can be found in **openstack_dashboard/local/local_settings.py**. This file holds sensible defaults for a common installation but you might need to tweek them to fit your use case.


If you are running Keystone on your own machine the address will be 'http://localhost:5000/v3'. If Keystone is configured to run on a different port and/or address you should set this acordingly.

<pre>
 OPENSTACK_HOST = "Keystone server IP address"
 OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3" % OPENSTACK_HOST
</pre>

- Configure these for your outgoing email host or leave the default values for the console email backend. More details on how to configure this can be found [in the Django docs](https://docs.djangoproject.com/en/1.8/topics/email/)

<pre>
 EMAIL_HOST = 'smtp.my-company.com'
 EMAIL_PORT = 25
 EMAIL_HOST_USER = 'djangomail'
 EMAIL_HOST_PASSWORD = 'top-secret!'
 EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
</pre>

- Keystone Account for the IdM to perform tasks like user registration.

<pre>
 OPENTACK_KEYSTONE_ADMIN_CREDENTIALS = {
  'USERNAME': 'the_username',
  'PASSWORD': 'the_password',
  'PROJECT': 'the_projectname',
 }
</pre>

- User Registration settings

<pre>
 EMAIL_LIST_TYPE
</pre>

This settings allows for email domain filtering on user registration. Set to 'whitelist', 'blacklist' or comment it out for no filtering.

- noCAPTCHA reCAPTCHA. Get your keys [here](https://www.google.com/recaptcha/admin#createsite). More documentation in [the package repository](https://github.com/ImaginaryLandscape/django-nocaptcha-recaptcha)

<pre>
 USE_CAPTCHA = False
 NORECAPTCHA_SITE_KEY   = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
 NORECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
</pre>


- FIWARE Applications and Roles. These settings map applications used in the FIWARE-Lab environment and are needed for automated tasks, for example granting the **Purchaser** role in the **Store** to any created organization. Depending on your use case you might need or want to modifiy them, but normal installations in a *fiware-like* environment won't need to change the following code. Keep in mind that if your use case differs too much you might need to change the code to prevent some of these operations. If you are not using the scripts you will need to check the ids in through the API or in the database yourself.

<pre>
 FIWARE_PURCHASER_ROLE_ID = 'id'
 FIWARE_PROVIDER_ROLE_ID = 'id'
 FIWARE_IDM_ADMIN_APP = 'idm'
 FIWARE_CLOUD_APP = 'Cloud'
 FIWARE_DEFAULT_CLOUD_ROLE_ID = 'id'
 FIWARE_DEFAULT_APPS = [
  'Store',
 ]
</pre>


- Keystone roles. These settings map to normal keystone roles that are used by the IdM. As with the FIWARE Applications and Roles settings, they depend on your use case.

<pre>
 KEYSTONE_OWNER_ROLE = 'owner'
 KEYSTONE_TRIAL_ROLE = 'trial'
 KEYSTONE_BASIC_ROLE = 'basic'
 KEYSTONE_COMMUNITY_ROLE = 'community'
 MAX_TRIAL_USERS = 100
 OPENSTACK_KEYSTONE_ADMIN_ROLES = [
 KEYSTONE_OWNER_ROLE,
  'admin',
 ]
</pre>
 
#### **3. Django settings**

The settings for all the Django configuration are located at **horizon/openstack_dashboard/settings.py**

Here we added some django apps, middleware, etc. You can check the file for reference but there is no configuration to be done here.

#### **4. Running a development server**

To run a simple server to try out and check the IdM installation or for developping purpuses you can use Django's development server that comes with the IdM installation, which will automatically run in port 8000:

<pre>
 $ sudo tools/with_venv.sh python manage.py runserver
</pre>

You can also explicitly run:

<pre>
 $ sudo tools/with_venv.sh python manage.py runserver IP:8000
</pre>

For more documentation about this server, head to [django docs](https://docs.djangoproject.com/en/1.7/ref/django-admin/#django-admin-runserver)

**IMPORTANT NOTE**: From the Django-runserver documentation: DO NOT USE THIS SERVER IN A PRODUCTION SETTING. It has not gone through security audits or performance tests.

### Installing Keystone

#### **1. Install Ubuntu dependencies and repository**

- Get the code

<pre>
 $ git clone https://github.com/ging/keystone.git
 $ cd keystone
</pre>

- Install the system dependencies:

<pre>
 $ sudo apt-get install python-dev libxml2-dev libxslt1-dev libsasl2-dev libsqlite3-dev libssl-dev libldap2-dev libffi-dev
</pre>

- Python dependencies

<pre>
  $ sudo python tools/install_venv.py
</pre>

- To verify that this has worked correctly:

<pre>
 $ source .venv/bin/activate
 $ python
 >>> import keystone
 >>>
</pre>

- Create the default configuration file

<pre>
 $ cp etc/keysonte.conf.sample etc/keystone.conf
</pre>

**Note:** If you want to use a mysql database you will need to run the following command, as python mysql library is not included by default in keystone:

<pre>
 $ sudo tools/with_venv.sh pip install mysql-python 
</pre>

#### **2. Keystone configuration**

After creating the default configuration file, the following lines must be uncommented:

<pre>
  admin_token=ADMIN
  admin_port=35357
  public_port=5000
</pre>

Run the following commands to create the database:

<pre>
 $ sudo tools/with_venv.sh bin/keystone-manage db_sync
</pre>

Create tables for the OAuth2.0 extension
  
<pre>
  $ sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=oauth2 
</pre>

Create tables for the Fiware Roles extension
  
<pre>
  $ sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=roles
</pre>

Create tables for the User Registration extension
  
<pre>
  $ sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=user_registration 
</pre>

#### **3. Run Keystone**

To run Keystone, we must either run it as a service o with the given commands:

<pre>
  $ sudo tools/with_venv.sh bin/keystone-all -v
</pre>

The last parameter (-v) is optional, but it will give you a more detailed view on what is happening with each call to the server.

Configuring Keystone as a service will be shown later on.

#### **4. Initial Data**

For the Identity Manager to work, the database has to be populated with some initial data. To populate the database we provide a script in the official KeyRock repository, along with other management tools. Take a  look at the following project for the automatic installation, configuration and sample utilities at https://github.com/ging/idm_deployment. For this initial data, use the task keystone.populate. Additionally, there is a task called keystone.test_data that will create some sample data to start using the Identity Manager right away, for demo or test purposes.

#### **5. Configuring Keystone as a service**

If you want to ad the keystone to init.d to run it as a service there are serveral possibilities. You can try to reuse the scripts provided with keystone or you can add a .conf file to **etc/init**.
Here is a basic example:

Create the following file at: **etc/init/keystone_idm.conf**

<pre>
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
</pre>

To run keystone, you can now run it with the following command:

<pre>
  $ sudo service keystone_idm start
</pre>

#### **6. Running tests**

In order to test, we use the keystone built in system: **tox** and **testr**.

To execute all tests:

<pre>
  $ sudo tox
</pre>

To Execute the extension tests (in this case for oauth2):

<pre>
 $ sudo tox -e py27 -- keystone.tests.test_v3_oauth2
</pre>

To debug during test, add the following to the command:

<pre>
 -e debub
</pre>

Debugging the extensions is not possible, therefore we must run the keystone service (or with the keystone-all command) and making calls from another terminal

## System Administration

### White and black lists

As administrator of IdM KeyRock you can manage white and black lists in order to allow and deny access to users by their email domains.

There is a file for each of the list which you can find at **/horizon/openstack_dashboard/fiware_auth/blacklist.txt** or **whitelist.txt**.

- Whitelist

Add a line for each of the domains that are allowed. No other domain will be allowed to register users.

- Blacklist

Add a line for each of the domains that are not allowed. If a user has an email from this domain, they will not be able to register.

## Sanity Check Procedures
The Sanity Check Procedures are the steps that a System Administrator will take to verify that an installation is ready to be tested. This is therefore a preliminary set of tests to ensure that obvious or basic malfunctioning is fixed before proceeding to unit tests, integration tests and user validation.

### End to End testing

1. Verify that the host address of IdM can be reached. By default, web access will show a Login Page.

2. Acquire a valid username and password and access with those credentials. The resulting web page is the landing page of the IdM KeyRock Portal.

3. Verify that you can view the list of applications, organizations, etc.

### List of Running Processes

In you have run the Horizon and Keystone run commands without errors, the portal is up and running.

### Network interfaces Up & Open

- TCP port 80 should be accessible to the web browsers in order to load the IdM Portal (8000 for development).
- Ports 5000 and 35357 are Keystone's public and admin port respectively.

### Databases

If you have correctly populated the database when installing the GE, the connection with it is up and running.

The databases and tables needed are:

<pre>
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
</pre>

## Diagnosis Procedures

The Diagnosis Procedures are the first steps that a System Administrator will take to locate the source of an error in a GE. Once the nature of the error is identified with these tests, the system admin will very often have to resort to more concrete and specific testing to pinpoint the exact point of error and a possible solution. Such specific testing is out of the scope of this section.

### Resource availability

* Verify that 2.5MB of disk space is left using the UNIX command 'df'

### Remote Service Access

Please make sure port 80 is accessible (port 8000 in development mode).

### Resource consumption

Typical memory consumption is 100MB and it consumes almost the 1% of a CPU core of 2GHz, but it depends on user demand.

### I/O flows

Clients access the KeyRock Interface through the client's Web Browser. This is simple HTTP traffic. It makes requests to the local database.