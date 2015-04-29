idm_deployment
==============

Set of tools to help in developing, deploying and testing FIWARE's IdM KeyRock using [Fabric](http://www.fabfile.org/).

The IdM is made out of two components, the web-based front-end and the restful back-end. You can check specific documentation in their repos
[ging/keystone](https:/github.com/ging/keystone)
[ging/horizon](https:/github.com/ging/horizon)

### Installation
Create a settings file
```
cp conf/settings.py.example conf/settings.py
```
Install dependencies.
Please, check the project wikis for specific documentation and dependencies. This section only covers the tools dependencies.

#### virtualenvwrapper
Follow the instructions here https://virtualenvwrapper.readthedocs.org/en/latest/index.html

Create a virtualenv and activate it
```
mkvirtualenv idm_deployment
```
Install python dependencies
```
pip install -r requirements.txt
```

### Configuration
There is a configuration file in /conf/settings.py.example. Check the wiki for the details about each option.

### Usage
**right now only localhost command works, dont use keystonehost or horizonhost**  
To see all available commands use 
```
fab --list
```

With the virtualenv activated (use [workon](https://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html?highlight=workon)) you can run the commands using fab task1 task2. The first task must always be one to set the target host (localhost for example). The second task can be any of the other tasks. 
For example: 
```
fab keystonehost keystone.populate
```

Some tasks accept arguments that override the defaults from conf/settings.py. It is recommended to use settings.py to configure the tasks but you can use this arguments in a per-task basis if you find you need it.
For example: 
```
fab localhost keystone.deploy:dev=True
```

Use the -p option to prevent Fabric from asking you for your password on every command when executing tasks on remote hosts:
```
-p PASSWORD, --password=PASSWORD

Sets env.password to the given string; it will then be used as the default password when making SSH connections or calling the sudo program.
```
