#!/bin/bash

# Install Ubuntu dependencies
sudo apt-get update
sudo apt-get install -y wget python python-dev git
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

# Install virtualenvwrapper and virtualenv
sudo pip install virtualenvwrapper
export WORKON_HOME=~/venvs
mkdir -p $WORKON_HOME

echo "
# Settings for VirtualenvWrapper
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
" >> .profile
source .profile

echo "
# Settings for VirtualenvWrapper
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
" >> .bashrc
source .bashrc

# Download latest version of the code 
git clone https://github.com/ging/fiware-idm idm
cd idm
cp conf/settings.py.example conf/settings.py

# Create virtualenv
mkvirtualenv idm_tools

# Install python dependecies
pip install -r requirements.txt

# Install Keystone back-end and set-up service
fab keystone.install
fab keystone.database_create
fab keystone.set_up_as_service
sudo service keystone_idm start
fab keystone.populate

# Install Horizon front-end and set-up service
fab horizon.install
fab horizon.set_up_as_service
sudo service horizon_idm start