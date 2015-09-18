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
from fabric.colors import red, green

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
def update(horizon_path=settings.HORIZON_ROOT):
    """Update the Front-end and its dependencies."""
    print 'Updating Horizon...'
    with lcd(horizon_path):
        lrun('git pull origin')
        lrun('sudo python tools/install_venv.py')
    print green('Horizon updated.')
    if not check(horizon_path):
        return 0 # flag for the main task
    else:
        return 1 # flag for the main task

@task
def check(horizon_path=settings.HORIZON_ROOT):
    """Checks for new settings in the template which don't exist in the current file"""

    print 'Checking Horizon...',
    path = horizon_path + 'openstack_dashboard/local/'
    with open(path+'local_settings.py','r') as old_file, open(path+'local_settings.py.example','r') as new_file:
        old = set(old_file)
        new = set(new_file)
    c1 = set()
    c2 = set()

    for s in new.difference(old):
        if s.find('=') != -1:
            c1.add(s[0:s.find('=')])
    for s in old.difference(new):
        if s.find('=') != -1:
            c2.add(s[0:s.find('=')])

    latest_settings = c1.difference(c2)
    if not latest_settings:
        print (green('Everything OK'))
        return 1 # flag for the main task
    else:
        print red('Some errors were encountered:')
        print red('The following settings couldn\'t be found in your local_settings.py module:')
        for i in latest_settings:
            print '\t'+red(i)
        print red('Please edit the local_settings.py module manually so that it contains the settings above.')
        return 0 # flag for the main task

@task
def dev_server(address=settings.HORIZON_DEV_ADDRESS,
               horizon_path=settings.HORIZON_ROOT):
    """Run horizon server for development purposes"""
    with lcd(horizon_path):
        lrun(('sudo tools/with_venv.sh python manage.py runserver '
                 '{0}').format(address))
        