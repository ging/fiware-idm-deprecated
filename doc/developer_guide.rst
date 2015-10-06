*********************************
Developers and contributors Guide
*********************************

.. contents::
   :local:
   :depth: 3

Introduction
============

The intent of this guide is to cover more in-depth the implementation
details, settings, problems encountered and their solutions, etc. of
KeyRock to help developers that want to contribute or modify the code
for their own custom use-cases. Additionally to this, all the components
(Keystone, Horizon, the modified KeystoneClient library, etc.) can
generate their own specific documentation using Sphinx with autodocs and
code-level comments.

Horizon
=======

This section covers all the Horizon related concepts.

Settings and Configuration
--------------------------

The base Horizon from OpenStack is a complex project and comes with lots
of settings and several settings files. Some of them require
configuration for the IdM to work, others are fine with the default
values and a lot others are unused. In this section we are going to
cover the ones we need to set, for further reference please take a look
at the `official
documentation <http://docs.openstack.org/developer/horizon/topics/settings.html>`__

Local_settings 
^^^^^^^^^^^^^^

At openstack_dashboard/local/local_settings.py

- Identity API v3

We need to configure to use the Identity
API v3 in our Keystone. Only matters to us the identity value. For
example:

.. code-block:: python

   OPENSTACK_API_VERSIONS = {
   "data_processing": 1.1,
   "identity": 3,
   "volume": 2
   }

   OPENSTACK_HOST = "Keystone server IP address" 
   OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3" % OPENSTACK_HOST 

- Email
Configure these for your outgoing email host or leave the default values
for the console email backend

.. code-block:: python

   EMAIL_HOST = 'smtp.my-company.com'
   EMAIL_PORT = 25 
   EMAIL_HOST_USER = 'djangomail' 
   EMAIL_HOST_PASSWORD = 'top-secret!' 
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

- IdM account

Account for the IdM to perform tasks like user registration

.. code-block:: python

   OPENSTACK_KEYSTONE_ADMIN_CREDENTIALS = {
      'USERNAME': 'the_username',
      'PASSWORD': 'the_password',
      'PROJECT': 'the_projectname',
   }


-  FIWARE Applications and Roles. 

These settings map to applications
used in the FIWARE-Lab environment and are needed for automated
tasks, for example granting the **Purchaser** role in the **Store**
to any created organization. Depending on your use case you might
need or want to modify them but normal installations in a
*fiware-like * environment wont need to change anything. Keep in mind
that if your use case differs too much you might need to change the
code to prevent some of this operations.

.. code-block:: python

   FIWARE_PURCHASER_ROLE_ID = 'the_id'
   FIWARE_PROVIDER_ROLE_ID = 'the_id'
   FIWARE_IDM_ADMIN_APP = 'idm'
   FIWARE_CLOUD_APP = 'Cloud'
   FIWARE_DEFAULT_CLOUD_ROLE_ID = 'the_id'
   FIWARE_DEFAULT_APPS = [
     'Store',
   ]

-  Keystone roles. 

These settings map to normal keystone roles that are
used by the IdM. As with the FIWARE Application and Roles settings,
they depend on your use case.

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

Django settings.py
^^^^^^^^^^^^^^^^^^
At **openstack_dashboard/settings.py**

We added some django apps, middleware, etc. You can check the file for
reference but there is no configuration to be done there.

Keystone
========


django_openstack_auth
=======================