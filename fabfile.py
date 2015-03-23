# Copyright (C) 2014 Universidad Politecnica de Madrid
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from deployment import keystone
from deployment import horizon
from deployment import migration
from conf import settings

from fabric.operations import local as lrun, run
from fabric.context_managers import lcd, cd
from fabric.api import task
from fabric.state import env

@task
def localhost():
    """Run the task in local machine."""
    env.cd = lcd
    env.run = lrun
    env.hosts = ['localhost']

@task
def keystonehost():
    """Run the task in the keystone machine.
    To change it, modify deployment:conf:settings.py
    """
    env.cd = cd
    env.run = run
    env.hosts = settings.HOSTS['keystone']

@task
def horizonhost():
    """Run the task in the horizon machine.
    To change it, modify deployment:conf:settings.py
    """
    env.cd = cd
    env.run = run
    env.hosts = settings.HOSTS['horizon']

def set_up(dev=False):
    """Install system and python dependencies."""
    _install_dependencies()

def _install_dependencies():
    command = settings.UBUNTU_DEPENDENCIES['install_command']
    dependencies = ' '.join(settings.UBUNTU_DEPENDENCIES['dependencies'])
    env.run('{command} {dependencies}'.format(command=command, 
        dependencies=dependencies))
    print 'Dependencies correctly installed'