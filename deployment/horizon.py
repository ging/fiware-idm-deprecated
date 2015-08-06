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

import string
import os

from fabric.api import task
from conf import settings
from fabric.context_managers import lcd
from fabric.operations import local as lrun

@task
def install(horizon_path=settings.HORIZON_ROOT):
    """Download and install the Front-end and its dependencies."""
    if os.path.isdir(horizon_path[:-1]):
        print 'Already downloaded.'
    else:
        lrun('git clone https://github.com/ging/horizon.git \
            {0}'.format(horizon_path))

    with lcd(horizon_path):
        dependencies = ' '.join(settings.UBUNTU_DEPENDENCIES['horizon'])
        lrun('sudo apt-get install {0}'.format(dependencies))
        lrun('sudo python tools/install_venv.py')

    path = horizon_path + '/openstack_dashboard/local/'
    class Template(string.Template):
        delimiter = '$$'
    template_settings = Template(open(path + 'local_settings.py.example').read())
    out_file = open(path + "local_settings.py", "w")
    out_file.write(
        template_settings.substitute({
            'IDM_NAME': settings.IDM_USER_CREDENTIALS['username'],
            'IDM_PASS': settings.IDM_USER_CREDENTIALS['password'],
            'IDM_PROJECT': settings.IDM_USER_CREDENTIALS['project'],
            'KEYSTONE_ADDRESS': settings.KEYSTONE_INTERNAL_ADDRESS,
            'KEYSTONE_PUBLIC_PORT':settings.KEYSTONE_PUBLIC_PORT,
        }))
    out_file.close()

@task
def dev_server(address=settings.HORIZON_DEV_ADDRESS,
               horizon_path=settings.HORIZON_ROOT):
    """Run horizon server for development purposes"""
    with lcd(horizon_path):
        lrun(('sudo tools/with_venv.sh python manage.py runserver '
                 '{0}').format(address))
        