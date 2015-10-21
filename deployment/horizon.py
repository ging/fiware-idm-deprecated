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
from fabric.colors import red, green, yellow
from fabric.tasks import Task

@task
def install(horizon_path=settings.HORIZON_ROOT, version=None):
    """Download and install the Front-end and its dependencies."""
    if os.path.isdir(horizon_path[:-1]):
        print 'Already downloaded.'
    else:
        lrun('git clone https://github.com/ging/horizon.git \
            {0}'.format(horizon_path))

    with lcd(horizon_path):
        if not version:
            version = settings.KEYROCK_VERSION
        
        lrun('git checkout tags/keyrock-{0}'.format(version))

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

    instance.run(horizon_path=horizon_path) # run check task

@task
def update(horizon_path=settings.HORIZON_ROOT):
    """Update the Front-end and its dependencies."""
    # returns 1 if everything went OK, 0 otherwise

    print 'Updating Horizon...'
    with lcd(horizon_path):
        lrun('git pull origin')
        lrun('sudo python tools/install_venv.py')
    print green('Horizon updated.')
    return instance.run(horizon_path=horizon_path) #flag for the main task

@task
def dev_server(address=settings.HORIZON_DEV_ADDRESS,
               horizon_path=settings.HORIZON_ROOT):
    """Run horizon server for development purposes"""
    with lcd(horizon_path):
        lrun(('sudo tools/with_venv.sh python manage.py runserver '
              '{0}').format(address))  

@task
def set_up_as_service(absolute_horizon_path=None):
    if not absolute_horizon_path:
        absolute_horizon_path = os.getcwd() + '/' + settings.HORIZON_ROOT
    in_file = open('conf/horizon_idm.conf')
    src = string.Template(in_file.read())
    out_file = open("tmp_horizon_idm.conf", "w")
    out_file.write(src.substitute({
        'absolute_horizon_path': absolute_horizon_path}))
    out_file.close()
    lrun('sudo cp tmp_horizon_idm.conf /etc/init/horizon_idm.conf')
    lrun('sudo rm tmp_horizon_idm.conf')
    lrun('sudo ln -s /etc/init/horizon_idm.conf /etc/init.d/horizon_idm')

class CheckTask(Task):
    """Run several checks in the Front-end settings file."""
    name = "check"
    def run(self, horizon_path=settings.HORIZON_ROOT, warnings=False):
        #   returns 1 if everything went OK, 0 otherwise
        print 'Checking Horizon... ',
        check1 = self._check_for_new_settings(horizon_path + 'openstack_dashboard/local/',warnings)
        check2 = self._check_for_roles_ids(horizon_path + 'openstack_dashboard/local/')
        return check1 and check2

    def _parse_setting(self, setting):
        if '=' in setting:
            if '#' in setting:
                if setting[1] == ' ':
                    return setting[setting.find('#')+2:setting.find('=')]
                else:
                    return setting[setting.find('#')+1:setting.find('=')]
            else:
                if setting[1] == ' ':
                    return setting[1:setting.find('=')]
                return setting[0:setting.find('=')]

    def _check_for_new_settings(self, settings_path, warnings=False):
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
            new_settings.add(self._parse_setting(s))
        for s in old.difference(new):
            old_settings.add(self._parse_setting(s))

        latest_settings = new_settings.difference(old_settings)

        created_settings = old_settings.difference(new_settings)

        if warnings and created_settings:
            print yellow('[Warning] the followind settings couldn\'t be found in the settings template: ')
            for s in created_settings:
                print '\t'+yellow(s)

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

        if not hasattr(settings,'INTERNAL_ROLES_IDS'):
            print red("INTERNAL_ROLES_IDS attribute could not be found. Please make sure you have completely installed Keystone before running this check.")
            return 0

        with open(settings_path+'local_settings.py', 'r') as local_settings:
            error = False
            for line in local_settings.readlines():
                if 'FIWARE_PURCHASER_ROLE_ID' in line and\
                settings.INTERNAL_ROLES_IDS['purchaser'] not in line:
                    error = True
                elif 'FIWARE_PROVIDER_ROLE_ID' in line and\
                settings.INTERNAL_ROLES_IDS['provider'] not in line:
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