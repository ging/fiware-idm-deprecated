#!/bin/bash

cd /opt

# Install Ubuntu dependencies
sudo apt-get update && \
	sudo apt-get install -y wget python python-dev git && \
	wget https://bootstrap.pypa.io/get-pip.py && \
	python get-pip.py

# Install virtualenvwrapper
pip install virtualenvwrapper && \
    export WORKON_HOME=~/venvs && \
    mkdir -p $WORKON_HOME

# Download latest version of the code 
git clone https://github.com/ging/fiware-idm idm && \
    cd idm && \
    cp conf/settings.py.example conf/settings.py

cd /opt/idm

# Install python dependecies
source /usr/local/bin/virtualenvwrapper.sh && \
    mkvirtualenv idm_tools2 && \
    pip install -r requirements.txt

# Install Keystone back-end
source /usr/local/bin/virtualenvwrapper.sh && \
    workon idm_tools2 && \
    fab keystone.install && \
    fab keystone.database_create

# Install Horizon front-end
source /usr/local/bin/virtualenvwrapper.sh && \
    workon idm_tools2 && \
    fab horizon.install