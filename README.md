idm_deployment
==============

Automated deployment for FIWARE's IdM using Fabric(http://www.fabfile.org/)

This fabric script is used to install Keystone and Horizon. The file has different commands that allows different actions, with wrappers to call multiple actions at once.

To deploy:

- fab idm_deploy:
    Calls horizon_deploy, keystone_deploy

Horizon Actions:

- fab horizon_deploy:
    Calls horizon_install, horizon_runserver

- fab horizon_install:
    Installs horizon from GitHub repository 'ging/horizon'
    Configures horizon according to said repository.

- fab horizon_runserver(:ip='yourip'):
      Runs server on the 'ip' if used or on localhost by default.

Keystone Actions:

- fab keystone_deploy:
        Calls keystone_install, keystone_service_create, keystone_database_create,keystone_service_start, keystone_database_init

- fab keystone_reset:
        Convenience wrapper to reset to a clean installation in development. Calls keystone_service_stop, keystone_database_delete, keystone_database_create,keystone_service_start, keystone_database_init

- fab keystone_install:
        Installs keystonse from GitHub repostitory 'ging/keystone'
        Creates keystone.conf file and configures it according to repository.

- fab keystone_service_create:
        Adds keystone to init.d to run as a service.
        Keystone can be run using: sudo service keystoneoauth2 start
        And can be stopped: sudo service keystoneoauth2 stop

- fab keystone_service_start:
        Starts keystone service

- fab keystone_service_stop:
        Stops keystone service

- fab keystone_database_create:
        Creates database including the oauth2 and fiware_roles extensions.

- fab keystone_database_init:
        Initial data using keystone v3 and incorporating oauth2 and roles. Requires keystone to be running.

- fab keystone_database_delete:
        Deletes existing dababase with all data

- fab keystone_sample_data:
        Runs the sample_data file given in keystone. This command should not be used for IdM, 'fab keystone_database_init' should be used instead, which used Keystone v3. Requires keystone to be running.