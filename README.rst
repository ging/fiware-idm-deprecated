***********************************
Identity Manager - Keyrock Overview
***********************************

.. contents::
   :local:
   :depth: 3

.. _introduction:

Introduction
============

This project is part of `FIWARE <http://fiware.org>`__. You will find
more information about this FIWARE GE
`here <http://catalogue.fiware.org/enablers/identity-management-keyrock>`__.

-  You will find the source code of this project in GitHub `here <https://github.com/ging/fiware-idm>`__
-  You will find the documentation of this project in Read the Docs `here <http://fiware-idm.readthedocs.org/>`__

Welcome to the main repository for the UPM's implementation of the
FIWARE Identity Manager Generic Enabler. This repository acts as an
entry point and holds the documentation and some automated tools for
installation and management. The IdM is composed of two independent
components, a RESTful back-end and web front-end.

If you want to see the
code for each of the components of the IdM and more specific
documentation please head to each component's repository:

-  Horizon based front-end `ging/horizon <https://github.com/ging/horizon>`__
-  Keystone based back-end `ging/keystone <https://github.com/ging/keystone>`__

You can see a working installation in the FIWARE Lab sandbox environment
https://account.lab.fiware.org/

.. begin-requirements

Requirements
------------

Identity Manager - KeyRock requires Ubuntu 12.04 or greater.

Both Horizon, for the front-end, and Keystone, for the back-end, must be
installed in order for the generic enabler to run correctly. They can be installed
in the same machine or in two separated ones. If you choose to separate them, the
two machines must be able to communicate to each other through the network.

.. end-requirements

.. _build:

How to Build & Install
======================

The IdM is made out of two components, the web-based front-end and the
restful back-end. You can check specific documentation in their respective repositories.


Installing the back-end
-----------------------

.. begin-keystone-installation

Install the dependencies

::

    $ sudo apt-get install python python-dev python-virtualenv libxml2-dev libxslt1-dev libsasl2-dev libssl-dev libldap2-dev libffi-dev libsqlite3-dev libmysqlclient-dev python-mysqldb


Get the code

:: 

    $ git clone https://github.com/ging/keystone && cd keystone
  

Install the python dependencies

::

  $ sudo python tools/install_venv.py


Create a configuration file

::

  $ cp etc/keystone.conf.sample etc/keystone.conf

Create the tables and populate the database

.. begin-database

::
    
    $ sudo tools/with_venv.sh bin/keystone-manage -v db_sync
    $ sudo tools/with_venv.sh bin/keystone-manage -v db_sync --extension=oauth2
    $ sudo tools/with_venv.sh bin/keystone-manage -v db_sync --extension=roles
    $ sudo tools/with_venv.sh bin/keystone-manage -v db_sync --extension=user_registration
    $ sudo tools/with_venv.sh bin/keystone-manage -v db_sync --extension=two_factor_auth
    $ sudo tools/with_venv.sh bin/keystone-manage -v db_sync --extension=endpoint_filter
    $ sudo tools/with_venv.sh bin/keystone-manage -v db_sync --populate

.. end-database

You can run keystone in the console

::

  $ sudo tools/with_venv.sh bin/keystone-all -v


You can now log into the web (if you have horizon installed) using the administrative account (by
default user idm and the password you entered during the populate step).

Finally, if you want to run the keystone backend in the backgroud you
can :ref:`install it as a service <keystone-as-service>`.

.. end-keystone-installation

Now, head to the :ref:`configuration instructions <keystone-configuration>`.

Installing the front-end
------------------------

.. begin-horizon-installation

Install the dependencies

::

    $ sudo apt-get install python python-dev python-virtualenv libssl-dev libffi-dev libjpeg8-dev


Get the code

:: 

    $ git clone https://github.com/ging/horizon && cd horizon


Create a configuration file

::

  $ cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py


Install the python dependencies

::

  $ sudo python tools/install_venv.py
  

You can check everything went OK running the development server, but you
won't be able to log in until you install the backend.

::

    $ sudo tools/with_venv.sh python manage.py runserver localhost:8000


Finally, if you want to run the horizon frontend in the backgroud you
can install it as a service or, for a production environment, run it under Apache.

.. end-horizon-installation

Now, head to the :ref:`configuration instructions <horizon-configuration>`.

.. _extras:

Other Installation options
--------------------------

Docker
^^^^^^

We provide a Docker image to facilitate you the building of this
GE.

-  `Here <https://github.com/ging/fiware-idm/tree/master/extras/docker>`__
   you will find the Dockerfile and the documentation explaining how to
   use it.
-  In `Docker Hub <https://hub.docker.com/r/fiware/idm/>`__ you
   will find the public image.

VM Image
^^^^^^^^
We provide an installation script that can be run within a Ubuntu
virtual machine. This script installs the whole Identity Manager, and
sets it up to run in background.

You can find the installation script and a verification script `here <https://github.com/ging/fiware-idm/tree/master/extras/scripts>`__.

Chef
^^^^
We also provide a Chef Cookbook, which you can find `here <https://github.com/ging/fiware-idm/tree/master/extras/chef>`__.


.. _api:

API Overview
=============

Keyrock back-end is based on Openstack
`Keystone <http://docs.openstack.org/developer/keystone/>`__ project, so
it exports all the Keystone API. However, Keyrock implements some custom
extensions that have their own REST APIs. Furthermore, to facilitate the
access to some identity resources we have enabled an `SCIM
2.0 <http://www.simplecloud.info/>`__ API.

Finally, one of the main uses of Keyrock is to allow developers to add
identity management (authentication and authorization) to their
applications based on FIWARE identity. This is posible thanks to
`OAuth2 <http://oauth.net/2/>`__ protocol.

-  `Keystone
   API <http://developer.openstack.org/api-ref-identity-v3.html>`__
-  `Keyrock extensions
   API <http://docs.keyrock.apiary.io/#reference/keystone-extensions>`__
-  `SCIM 2.0 API <http://docs.keyrock.apiary.io/#reference/scim-2.0>`__
-  `OAuth2 API <http://fiware-idm.readthedocs.org/en/latest/oauth2.html>`__

You will find the full API description
`here <http://docs.keyrock.apiary.io/>`__


Changes introduced in 5.x
=========================

This section is for users of the 4.x versions. They biggest change introduced
in 5.x is the removal Fabric tasks. The functionality in the tasks has been moved elsewhere, converted to a CLI or removed completely.

- A new CLI tool to help with admin tasks. Documentation :ref:`here <cli-tools>`
- The instalation now is always done step by step.
- The population script for the keystone database is now part of keystone.

Check the release notes for a full list of changes and new features.

.. _advanced:

Advanced Documentation
======================

-  `User & Programmers
   Manual <http://fiware-idm.readthedocs.org/en/latest/user_guide.html>`__
-  `Installation & Administration
   Guide <http://fiware-idm.readthedocs.org/en/latest/admin_guide.html>`__
-  `Production set-up
   guide <http://fiware-idm.readthedocs.org/en/latest/setup.html>`__
-  `How to run
   tests <http://fiware-idm.readthedocs.org/en/latest/admin_guide.html#end-to-end-testing>`__
-  `Using the FIWARE LAB instance
   (OAuth2) <http://fiware-idm.readthedocs.org/en/latest/oauth2.html>`__
-  `Developers and contributors
   Guide <http://fiware-idm.readthedocs.org/en/latest/developer_guide.html>`__

