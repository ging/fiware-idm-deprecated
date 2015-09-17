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

from fabric.api import task
from fabric.operations import local as lrun
from fabric.colors import green


@task
def localhost():
    """DEPRECATED. Executing tasks in remote hosts is no longer supported.
    Therefore, localhost task is no longer required. Call the tasks directly."""
    print localhost.__doc__


def set_up(dev=False):
    """Install system and python dependencies."""
    _install_dependencies()

def _install_dependencies():
    command = settings.UBUNTU_DEPENDENCIES['install_command']
    dependencies = ' '.join(settings.UBUNTU_DEPENDENCIES['dependencies'])
    lrun('{command} {dependencies}'.format(command=command, 
        dependencies=dependencies))
    print 'Dependencies correctly installed'

@task
def update_all(keystone_path=settings.KEYSTONE_ROOT, horizon_path=settings.HORIZON_ROOT):
    keystone.update(keystone_path)
    horizon.update(horizon_path)
    print(green('Everything up to date!'))

@task
def check_all(keystone_path=settings.KEYSTONE_ROOT, horizon_path=settings.HORIZON_ROOT):
    keystone.check(keystone_path)
    horizon.check(horizon_path)