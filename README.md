# Identity Manager - Keyrock

+ [Introduction](#def-introduction)
+ [How to Build & Install](#def-build)
    - [Docker](#def-docker)
+ [API Overview](#def-api)
+ [Advanced documentation](#def-advanced)

---

<br>

<a name="def-introduction"></a>
## Introduction

This project is part of [FIWARE](http://fiware.org). You will find more information abour this FIWARE GE [here](http://catalogue.fiware.org/enablers/identity-management-keyrock).

- You will find the source code of this project in GitHub [here](https://github.com/ging/fiware-idm)
- You will find the documentation of this project in Read the Docs [here](http://fiware-idm.readthedocs.org/)

Wellcome to the main repository for the UPM's implementation of the FIWARE Identity Manager Generic Enabler. This repository acts as an entry point and holds the documentation and some automated tools for installation and management. The IdM is composed of two independent components, a RESTful back-end and web front-end. If you want to see the code for each of the components of the IdM and more specific documentation please head to each component's repository:  

Horizon based front-end [ging/horizon](https://github.com/ging/horizon)  
Keystone based back-end [ging/keystone](https://github.com/ging/keystone)    

You can see a working installation in the FIWARE Lab sandbox environment https://account.lab.fiware.org/ 


<a name="def-build"></a>
## How to Build & Install

In this repository you can find a set of tools to help in developing, deploying and testing FIWARE's IdM KeyRock using [Fabric](http://www.fabfile.org/). This is the recomended way to install the IdM but if you rather install it step by step on your own, please head to the advanced documentation.

The IdM is made out of two components, the web-based front-end and the restful back-end. You can check specific documentation in their repos.


### Tools installation
For the instructions on how to install the IdM using the tools scroll down to the next section. This section covers the tools installation.

Install python and python-dev
`sudo apt-get install python-dev `

Clone the tools in your machine  
```
git clone https://github.com/ging/fiware-idm idm && cd idm
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

**Configuration**  
There is a configuration file template in /conf/settings.py.example. This provides as a good base configuration file that should be enough for a test/development installation. Some options you might have to pay some attention to are:
* IDM_ROOT: if the location of the keystone and horizon components in your system is not directly inside the folder where you have cloned the tools you will have to set this accordingly.
* HORIZON_DEV_ADDRESS: sets the address and port where the frontend will listen to. Default is localhost:8000, you might want to tweak it based on your set up.
* KEYSTONE_ADMIN_PORT and KEYSTONE_PUBLIC_PORT: if you need to use different ports for the keystone back-end

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

*Front-end*  
```
fab horizon.install
```
You can check everything went OK running the development server, but you wont be able to log in until you install the backend.
```
fab horizon.dev_server
```

<a name="def-docker"></a>
### Docker

We also provide a Docker image to facilitate you the building of this GE.

- [Here](https://github.com/ging/fiware-idm/tree/master/docker) you will find the Dockerfile and the documentation explaining how to use it.
- In [Docker Hub](https://hub.docker.com/r/ging/fiware-idm/) you will find the public image.

<a name="def-api"></a>
## API Overview

Keyrock back-end is based on Openstack [Keystone](http://docs.openstack.org/developer/keystone/) project, so it exports all the Keystone API. However, Keyrock implements some custom extensions that have their own REST APIs. Furthermore, to facilitate the access to some identity resources we have enabled an [SCIM 2.0](http://www.simplecloud.info/) API. 

Finally, one of the main uses of Keyrock is to allow developers to add identity management (authentication and authorization) to their applications based on FIWARE identity. This is posible thanks to [OAuth2](http://oauth.net/2/) protocol.

 - [Keystone API](http://developer.openstack.org/api-ref-identity-v3.html)
 - [Keyrock extensions API](http://docs.keyrock.apiary.io/#reference/keystone-extensions)
 - [SCIM 2.0 API](http://docs.keyrock.apiary.io/#reference/scim-2.0)
 - [OAuth2 API](http://fiware-idm.readthedocs.org/en/latest/oauth2/)

You will find the full API description [here](http://docs.keyrock.apiary.io/)

<a name="def-advanced"></a>
## Advanced Documentation

  - [User & Programmers Manual](http://fiware-idm.readthedocs.org/en/latest/user_guide/)
  - [Installation & Administration Guide](http://fiware-idm.readthedocs.org/en/latest/admin_guide/)
  - [Production set-up guide](http://fiware-idm.readthedocs.org/en/latest/setup/)
  - [How to run tests](http://fiware-idm.readthedocs.org/en/latest/admin_guide#end-to-end-testing)
  - [Using the FIWARE LAB instance (OAuth2)](http://fiware-idm.readthedocs.org/en/latest/oauth2/)