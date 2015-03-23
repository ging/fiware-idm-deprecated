idm_deployment
==============

Set of tools for deploying and testing for FIWARE's IdM KeyRock using Fabric(http://www.fabfile.org/)

Dependencies
Before you can run any command you must install the following dependencies:

Configuration
There is a configuration file in /conf/settings.py. Check the wiki for the details about each option.

Usage
To see all available commands use fab --list

With the virtualenv activated you can run the commands using fab [task1] [task2]. The first task must always be one to set the target host (localhost for example). The second task can be any of the other tasks. 
For example: fab keystonehost keystone.populate

Some tasks accept arguments that override the defaults from conf/settings.py. It is recommended to use settings.py to configure the tasks but you can use this arguments in a per-task basis if you find you need it.
For example: fab localhost keystone.deploy:dev=True

