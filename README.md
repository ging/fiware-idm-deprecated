idm_deployment
==============

Automated deployment for FIWARE's IdM

This fabric script is used to install Keystone and Horizon. The file has different commands that allows different actions.

Actions:

- fab install_horizon:
      Installs horizon from GitHub repository 'ging/horizon'
      Configures horizon according to said repository.

- fab runserver(:ip='yourip'):
      Runs server on the 'ip' if used or on localhost by default.


- fab install_keystone:
        Installs keystonse from GitHub repostitory 'ging/keystone'
        Creates keystone.conf file and configures it according to repository.

- fab keystone_service:
        Adds keystone to init.d to run as a service.
        Keystone can be run using: sudo service keystoneoauth2 start
        And can be stopped: sudo service keystoneoauth2 stop

- fab start:
        Starts keystone service

- fab stop:
        Stops keystone service

- fab database:
        Creates database including the oauth2 and fiware_roles extensions.

- fab data:
        Creates initial data taken from the sample_data file given in keystone
        This command should not be used for IdM, 'fab initial_data' should be used instead, which used Keystone v3.

- fab initial_data:
        Initial data using keystone v3 and incorporating oauth2 and roles.

- fab remove_database:
        Deletes existing dababase with all data

- fab restart:
        Stops keystone, deletes database (including initial data), creates new database with extensions, and starts service.

