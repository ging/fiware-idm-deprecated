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

import os

from fabric.api import run
from fabric.api import task
from deployment.conf import settings
from fabric.state import env

@task
def deploy(dev):
    """Fully installs the IdM frontend"""
    # TODO(garcianavalon) PARAMETERS!!!
    install(dev=dev)
    if dev:
        dev_server()
    else:
        # TODO(garcianavalon) production server!
        pass

@task
def install(horizon_path=settings.HORIZON_ROOT,
            dev=False):
    """Download and install Horizon and its dependencies."""
    print 'Installing frontend (Horizon)'

    if os.path.isdir(horizon_path[:-1]):
        print 'already downloaded'
    else:
        env.run('git clone https://github.com/ging/horizon.git \
            {0}'.format(horizon_path))

    with env.cd(horizon_path):
        if dev:
            env.run('git checkout development')

        env.run('sudo python tools/install_venv.py')
        env.run('cp openstack_dashboard/local/local_settings.py.example \
            openstack_dashboard/local/local_settings.py')
    print 'Done!'

@task
def dev_server(address=settings.HORIZON_DEV_ADDRESS,
               horizon_path=settings.HORIZON_ROOT):
    """Run horizon server for development purposes"""
    with env.cd(horizon_path):
        env.run('sudo tools/with_venv.sh python manage.py runserver \
            {0}'.format(address))