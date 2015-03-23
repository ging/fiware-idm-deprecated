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
from fabric.context_managers import cd


def deploy(fiwareclient_path, dev):
    """Fully installs the IdM frontend"""
    # TODO(garcianavalon) PARAMETERS!!!
    install(dev=dev)
    if dev:
        dev_server()
    else:
        # TODO(garcianavalon) production server!
        pass

def install(horizon_path, dev):
    """Download and install Horizon and its dependencies."""
    print 'Installing frontend (Horizon)'

    if os.path.isdir(horizon_path[:-1]):
        print 'already downloaded'
    else:
        run('git clone https://github.com/ging/horizon.git \
            {0}'.format(horizon_path))

    with cd(horizon_path):
        if dev:
            run('git checkout development')

        run('sudo python tools/install_venv.py')
        run('cp openstack_dashboard/local/local_settings.py.example \
            openstack_dashboard/local/local_settings.py')
    print 'Done!'

def dev_server(horizon_path, address):
    """Run horizon server for development purposes"""
    with cd(horizon_path):
        run('sudo tools/with_venv.sh python manage.py runserver \
            {0}'.format(address))