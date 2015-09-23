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
from fabric.operations import local as lrun, prompt
from fabric.colors import red, green
from fabric.tasks import Task

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
        lrun('sudo apt-get install -y {0}'.format(dependencies))
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
    # returns 1 if everything went OK, 0 otherwise

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
def dev_server(address=settings.HORIZON_DEV_ADDRESS,
               horizon_path=settings.HORIZON_ROOT):
    """Run horizon server for development purposes"""
    with lcd(horizon_path):
        lrun(('sudo tools/with_venv.sh python manage.py runserver '
              '{0}').format(address))      

class CheckTask(Task):

    name = "check"
    def run(self, horizon_path=settings.HORIZON_ROOT):
        #   returns 1 if everything went OK, 0 otherwise
        print 'Checking Horizon...',
        self._check_for_new_settings(horizon_path + 'openstack_dashboard/local/')
        self._check_for_roles_ids(horizon_path + 'openstack_dashboard/local/')

    def _check_for_new_settings(self, settings_path):
        """Checks for new settings in the template which don't exist in the current file"""
        # returns 1 if everything went OK, 0 otherwise
        with open(settings_path+'local_settings.py', 'r') as old_file,\
             open(settings_path+'local_settings.py.example', 'r') as new_file:
            old = set(old_file)
            new = set(new_file)

        new_settings = set()
        old_settings = set()

        # remove values to have settings' names
        for s in new.difference(old):
            if s.find('=') != -1:
                new_settings.add(s[0:s.find('=')])
        for s in old.difference(new):
            if s.find('=') != -1:
                old_settings.add(s[0:s.find('=')])

        latest_settings = new_settings.difference(old_settings)

        if not latest_settings:
            print green('Settings OK.'),
            return 1 # flag for the main task
        else:
            print red('Some errors were encountered:')
            print red('The following settings couldn\'t be found in your local_settings.py module:')
            settings_to_write = list()
            for s in latest_settings:
                with open(settings_path+'local_settings.py.example', 'r') as template:
                    block = 0
                    for line in template.readlines():
                        if s in line or block > 0:
                            settings_to_write.append(line)
                            if '{' in line: block += 1
                            if '}' in line: block -= 1
                print '\t'+red(s)

            autofix = prompt(red('Would you like to add defaults for the missing settings? [Y/n]: '),\
                             default='n', validate='[Y,n]')
            if autofix == 'Y':
                with open(settings_path+'local_settings.py', 'a') as output:
                    output.write('\n\n# --- NEW SETTINGS ADDED AUTOMATICALLY ---\n')
                    for s in settings_to_write:
                        output.write(s)
                print green('The missing settings were added.\nPlease check the local_settings.py module to make any necessary changes.')

            else:
                print red('Please edit the local_settings.py module manually so that it contains the settings above.')
            return 0 # flag for the main task

    def _check_for_roles_ids(self, settings_path):
        # returns 1 if everything went OK, 0 otherwise

        with open(settings_path+'local_settings.py', 'r') as local_settings:
            error = False
            for line in local_settings.readlines():
                if 'FIWARE_PURCHASER_ROLE_ID' in line and\
                line.split("FIWARE_PURCHASER_ROLE_ID = ")[1] !=\
                settings.INTERNAL_ROLES_IDS['purchaser']:
                    error = True
                elif 'FIWARE_PROVIDER_ROLE_ID' in line and\
                line.split("FIWARE_PROVIDER_ROLE_ID = ")[1] !=\
                settings.INTERNAL_ROLES_IDS['provider']:
                    error = True
                    break
        if not error:
            print green('Role IDs OK.')
            return 1
        else:
            autofix = prompt(red('Would you like to add the internal roles\' IDs to the local_settings.py module? [Y/n]: '), default='n', validate='[Y,n]')
            if autofix == 'Y':
                with open(settings_path+'local_settings.py', 'r+') as settings_file:
                    lines = settings_file.readlines()
                    settings_file.seek(0)
                    settings_file.truncate()
                    for line in lines:
                        if 'FIWARE_PURCHASER_ROLE_ID' in line:
                            line = 'FIWARE_PURCHASER_ROLE_ID = \''+settings.INTERNAL_ROLES_IDS['purchaser']+'\'\n'
                        if 'FIWARE_PROVIDER_ROLE_ID' in line:
                            line = 'FIWARE_PROVIDER_ROLE_ID = \''+settings.INTERNAL_ROLES_IDS['provider']+'\'\n'
                        settings_file.write(line)            
            return 0

instance = CheckTask()