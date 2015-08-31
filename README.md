# Identity Manager - Keyrock

+ [Introduction](#def-introduction)
+ [How to Build & Install](#def-build)
+ [API Overview](#def-api)
+ [Advanced documentation](#def-advanced)

---

<br>

<a name="def-introduction"></a>
## Introduction

This project is part of [FIWARE](http://fiware.org). You will find more information abour this FIWARE GE [here](http://catalogue.fiware.org/enablers/identity-management-keyrock).

Wellcome to the main repository for the UPM's implementation of the FIWARE Identity Manager Generic Enabler. This repository acts as an entry point and holds the [wiki](https://github.com/ging/fi-ware-idm/wiki) and some automated tools for installation and management. If you want to see the code for each of the components of the IdM and more specific documentation please head to each component's repository:  

Horizon based front-end https://github.com/ging/horizon  
Keystone based back-end https://github.com/ging/keystone  

You can see a working installation in the FIWARE Lab sandbox environment https://account.lab.fiware.org/ 


<a name="def-build"></a>
## How to Build & Install

In this repository you can find a et of tools to help in developing, deploying and testing FIWARE's IdM KeyRock using [Fabric](http://www.fabfile.org/). If you rather install it step by step on your own, please head to each component repository and follow their installation steps.

The IdM is made out of two components, the web-based front-end and the restful back-end. You can check specific documentation in their repos.

Back-end [ging/keystone](https://github.com/ging/keystone)  

Front-end [ging/horizon](https://github.com/ging/horizon)  

### Tools installation
For the instructions on how to install the IdM using the tools scroll down to the next section. This section covers the tools installation.

Install python and python-dev
`sudo apt-get install python-dev `

Clone the tools in your machine  
```
git clone https://github.com/ging/fi-ware-idm idm && cd idm
```

Create a settings file
```
cp conf/settings.py.example conf/settings.py
```

Install virtualenvwrapper. Follow the instructions here https://virtualenvwrapper.readthedocs.org/en/latest/index.html

Create a virtualenv and activate it
```
mkvirtualenv idm_tools
```
Install python dependencies
```
pip install -r requirements.txt
```

**Configuration**  
There is a configuration file template in /conf/settings.py.example. This provides as a good base configuration file that should be enough for a test/development installation. Some options you might have to pay some attention to are:
* IDM_ROOT: if the location of the keystone and horizon components in your system is not directly inside the folder where you have cloned the tools you will have to set this accordingly.
* HORIZON_DEV_ADDRESS: sets the address and port where the frontend will listen to. Default is localhost:8000, you might want to tweak it based on your set up.
* KEYSTONE_ADMIN_PORT and KEYSTONE_PUBLIC_PORT: if you need to use different ports for the keystone back-end

**Usage**  
To see all available commands use 
```
fab --list
```

With the virtualenv activated (use [workon](https://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html?highlight=workon)) you can run the commands using fab task_name.
For example: 
```
fab keystone.populate
```

Some tasks accept arguments that override the defaults from conf/settings.py. It is recommended to use settings.py to configure the tasks but you can use this arguments in a per-task basis if you find you need it. Other tasks might need explicit arguments like the path to a file. The way to pass arguments to tasks is simple and documented [here](http://docs.fabfile.org/en/1.10/tutorial.html#task-arguments)
For example: 
```
fab keystone.task:one_arg='this',another='that'
```

### Steps to install the IdM using the tools
*Front-end*  
```
fab horizon.install
```
You can check everything went OK running the development server, but you wont be able to log in until you install the backend.
```
fab horizon.dev_server
```
*Back-end*  
```
fab keystone.install
fab keystone.database_create
fab keystone.dev_server
```
You will need to populate the database with some data needed for the IdM to work properly. In another console and keeping the server on run
```
fab keystone.populate
```
You can now log into the web using the administrative account (by default user idm pass idm). If you want some more data to play around run keystone.test_data. This will create some users and organizations to make it easier to try the IdM. Log in with user0@test.com (default password test).
```
fab keystone.test_data
```
If at some point you want to clean up, run keystone.database_reset. It will delete the whole database, create it again and populate it.
```
fab keystone.database_reset
```
Finally, if you want to run the keystone backend in the backgroud you can install it as a service

```
fab keystone.set_up_as_service
```

<a name="def-api"></a>
## API Overview

Keyrock is based on Openstack [Keystone](http://docs.openstack.org/developer/keystone/) project. So it exports all the Keystone API. However, Keyrock implements some custom extensions that have their own REST APIs. Furthermore, to facilitate the access to some identity resources we have enabled an [SCIM 2.0](http://www.simplecloud.info/) API. 

Finally, one of the main uses of Keyrock is to allow developers to add identity management (authentication and authorization) to their applications based on FIWARE identity. This is posible thanks to [OAuth2](http://oauth.net/2/) protocol.

 - [Keystone API](http://developer.openstack.org/api-ref-identity-v3.html)
 - [Keyrock extensions API](http://docs.keyrock.apiary.io/#reference/keystone-extensions)
 - [SCIM 2.0 API](http://docs.keyrock.apiary.io/#reference/scim-2.0)
 - [OAuth2 API](https://github.com/ging/fi-ware-idm/blob/master/doc/oauth2.md)

You will find the full API description [here](http://docs.keyrock.apiary.io/)

<a name="def-api"></a>
## Advanced Documentation

- [User & Programmers Manual](https://github.com/ging/fi-ware-idm/tree/master/docs/user_guide.md)
- [Installation & Administration Guide](https://github.com/ging/fi-ware-idm/tree/master/docs/admin_guide.md)
- [Production set-up guide](https://github.com/ging/fi-ware-idm/blob/master/doc/setup.md)
- [How to run tests](https://github.com/ging/fi-ware-idm/tree/master/docs/)
- [Using the FIWARE LAB instance (OAuth2)](https://github.com/ging/fi-ware-idm/blob/master/doc/oauth2.md)