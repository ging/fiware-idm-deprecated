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

import ConfigParser
import string
import os
import random

from collections import namedtuple

from conf import settings

from keystoneclient.v3 import client

from fabric.api import task
from fabric.tasks import Task
from fabric.state import env
from fabric.api import execute


@task
def install(keystone_path=settings.KEYSTONE_ROOT, dev=False):
    """Download and install the Back-end and its dependencies."""
    if env.exists(keystone_path[:-1]):
        print 'already downloaded'
    else:
        env.run('git clone https://github.com/ging/keystone.git \
            {0}'.format(keystone_path))
    with env.cd(keystone_path):
        dependencies = ' '.join(settings.UBUNTU_DEPENDENCIES['keystone'])
        if dev:
            env.run('git checkout development')
            dependencies += ' ' + ' '.join(settings.UBUNTU_DEPENDENCIES['sqlite'])
        else:
            dependencies += ' ' + ' '.join(settings.UBUNTU_DEPENDENCIES['mysql'])
        
        env.run('sudo apt-get install {0}'.format(dependencies))
        env.run('sudo cp etc/keystone.conf.sample etc/keystone.conf')
        env.run('sudo python tools/install_venv.py')

        # Uncomment config file
        with env.cd('etc/'):
            env.run(("sudo sed -i "
                "'s/#admin_token=ADMIN/admin_token={0}/g' " 
                "keystone.conf").format(settings.KEYSTONE_ADMIN_TOKEN))
            env.run(("sudo sed -i "
                "'s/#admin_port=35357/admin_port={0}/g' "
                "keystone.conf").format(settings.KEYSTONE_ADMIN_PORT))
            env.run(("sudo sed -i "
                "'s/#public_port=5000/public_port={0}/g' "
                "keystone.conf").format(settings.KEYSTONE_PUBLIC_PORT))
    print 'Done!'

@task
def database_create(keystone_path=settings.KEYSTONE_ROOT, verbose=True,
                    mysql_user=False):
    if mysql_user:
        env.run('mysql -u {0} -p '.format(mysql_user))
        # TODO(garcianavalon) this is not executing inside mysql shell
        env.run('CREATE DATABASE {0};'.format(settings.KEYSTONE_PROD_DATABASE))
        # TODO(garcianavalon) grant all privileges!
        # TODO(garcianavlaon) connection string!!

    add_verbose = '-v' if verbose else ''
    with env.cd(keystone_path):
        env.run('sudo tools/with_venv.sh bin/keystone-manage {v} db_sync'.format(
            v=add_verbose))
        env.run('sudo tools/with_venv.sh bin/keystone-manage {v} db_sync \
            --extension=oauth2'.format(v=add_verbose))
        env.run('sudo tools/with_venv.sh bin/keystone-manage {v} db_sync \
            --extension=roles'.format(v=add_verbose))
        env.run('sudo tools/with_venv.sh bin/keystone-manage {v} db_sync \
            --extension=user_registration'.format(v=add_verbose))

@task
def database_delete(keystone_path=settings.KEYSTONE_ROOT,
                    keystone_db=settings.KEYSTONE_DEV_DATABASE,
                    mysql_user=False):
    if mysql_user:
        env.run('mysql -u {0} -p '.format(mysql_user))
        env.run('DROP DATABASE {0};'.format(settings.KEYSTONE_PROD_DATABASE))
    else:
        db_path = keystone_path + keystone_db
        if os.path.isfile(db_path):
            env.run('sudo rm ' + db_path)

@task
def database_reset(keystone_path=settings.KEYSTONE_ROOT, mysql_user=False):
    """Deletes keystone's database and create a new one, populated with
    the base data needed by the IdM. Requires a keystone instance running.
    """
    execute(database_delete, keystone_path=keystone_path, 
        mysql_user=mysql_user)
    execute(database_create, keystone_path=keystone_path, 
        mysql_user=mysql_user)
    execute('keystone.populate', keystone_path=keystone_path)


@task
def service_create(absolute_keystone_path=None):
    if not absolute_keystone_path:
        absolute_keystone_path = os.getcwd() + '/' + settings.KEYSTONE_ROOT
    in_file = open('conf/keystone_idm.conf')
    src = string.Template(in_file.read())
    out_file = open("tmp_keystone_idm.conf", "w")
    out_file.write(src.substitute({
        'absolute_keystone_path': absolute_keystone_path}))
    out_file.close()
    env.run('sudo cp tmp_keystone_idm.conf /etc/init/keystone_idm.conf')
    env.run('sudo rm tmp_keystone_idm.conf')

@task
def service_start():
    env.run('sudo service keystone_idm start')

@task
def service_stop():
    env.run('sudo service keystone_idm stop')

@task
def dev_server(keystone_path=settings.KEYSTONE_ROOT):
    """Runs the server in dev mode."""
    with env.cd(keystone_path):
        env.run('sudo tools/with_venv.sh bin/keystone-all -v')

class PopulateTask(Task):
    name = "populate"
    def run(self, keystone_path=settings.KEYSTONE_ROOT,
            internal_address=settings.CONTROLLER_INTERNAL_ADDRESS,
            public_address=settings.CONTROLLER_PUBLIC_ADDRESS,
            admin_address=settings.CONTROLLER_ADMIN_ADDRESS):

        config = self._get_keystone_config(keystone_path)
        keystone = self._admin_token_connection(config)

        # Keystone services
        self._create_endpoints(keystone, internal_address, public_address,
            admin_address, config)

        keystone_roles = self._create_keystone_roles(keystone)

        idm_user = self._create_idm_user_and_project(keystone, keystone_roles)
        
        idm_app = self._create_internal_roles_and_permissions(keystone)

        # Make the idm user administrator
        self._grant_administrator(keystone, idm_app, [idm_user])

    def _create_endpoints(self, keystone, internal_address, public_address,
                          admin_address, config):
        public_port = config.get('DEFAULT', 'public_port')
        admin_port = config.get('DEFAULT', 'admin_port')
        Endpoint = namedtuple('Endpoint', 'url interface')
        endpoints = [
            Endpoint('http://{public_address}:{port}/v3'
                     .format(public_address=public_address, port=public_port), 
                     'public'),
            Endpoint('http://{admin_address}:{port}/v3'
                     .format(admin_address=admin_address, port=admin_port), 
                     'admin'),
            Endpoint('http://{internal_address}:{port}/v3'
                     .format(internal_address=internal_address, port=public_port), 
                     'internal')
        ]
        service = keystone.services.create(name='keystone', type='identity',
            description='Keystone Identity Service')

        for endpoint in endpoints:
            keystone.endpoints.create(region='RegionOne',
                                      service=service,
                                      url=endpoint.url,
                                      interface=endpoint.interface)

        print 'Created Identity Service and Endpoints'    

    def _admin_token_connection(self, config):
        
        admin_port = config.get('DEFAULT', 'admin_port')
        token = config.get('DEFAULT', 'admin_token')

        endpoint = 'http://{ip}:{port}/v3'.format(ip='127.0.0.1',
                                                  port=admin_port)
        keystone = client.Client(token=token, endpoint=endpoint)
        print 'Connected to keystone using token'

        return keystone

    def _get_keystone_config(self, keystone_path):
        config = ConfigParser.ConfigParser()
        config.read(keystone_path + 'etc/keystone.conf')
        return config

    def _create_keystone_roles(self, keystone):
        # Default keystone roles
        # NOTE(garcianavalon) don't confuse it with keystone v2 API
        # default role (member_role_name=_member_). We need a default
        # role to add users to projects. Horizon knows this role throught
        # the local_settings.py file.
        keystone_roles = {
            'member': keystone.roles.create(name='member'),
            'owner': keystone.roles.create(name='owner'),
            'trial': keystone.roles.create(name='trial'),
            'basic': keystone.roles.create(name='basic'),
            'community': keystone.roles.create(name='community'),
            'admin': keystone.roles.create(name='admin', is_default=True),
        }
        print 'created default keystone roles'
        return keystone_roles

    def _create_idm_user_and_project(self, keystone, keystone_roles):
        idm_project = keystone.projects.create(
            name=settings.IDM_USER_CREDENTIALS['project'],
            description='',
            is_default=True,
            domain=settings.KEYSTONE_DEFAULT_DOMAIN)

        idm_user = keystone.users.create(
            name=settings.IDM_USER_CREDENTIALS['username'],
            username=settings.IDM_USER_CREDENTIALS['username'],
            password=settings.IDM_USER_CREDENTIALS['password'],
            default_project=idm_project,
            domain=settings.KEYSTONE_DEFAULT_DOMAIN)

        keystone.roles.grant(user=idm_user,
                             role=keystone_roles['admin'],
                             project=idm_project)
        keystone.roles.grant(user=idm_user,
                             role=keystone_roles['owner'],
                             project=idm_project)
        print 'Created default idm project and user.'

        return idm_user

    def _create_internal_roles_and_permissions(self, keystone):
        # Default internal application
        idm_app = keystone.oauth2.consumers.create(
            settings.IDM_USER_CREDENTIALS['username'], 
            description='',
            grant_type='authorization_code', 
            client_type='confidential', 
            is_default=True)

        # Default Permissions and roles
        created_permissions = []
        for permission in settings.INTERNAL_PERMISSIONS:
            created_permissions.append(
                keystone.fiware_roles.permissions.create(
                    name=permission, application=idm_app, is_internal=True))
        created_roles = []
        for role in settings.INTERNAL_ROLES:
            created_role = keystone.fiware_roles.roles.create(
                name=role, application=idm_app, is_internal=True)
            created_roles.append(created_role)
            # Link roles with permissions
            for index in settings.INTERNAL_ROLES[role]:
                keystone.fiware_roles.permissions.add_to_role(
                    created_role, created_permissions[index])

        print ('Created default fiware roles and permissions.')
        return idm_app

    def _grant_administrator(self, keystone, idm_app, users):
        provider_role = next(r for r
                        in keystone.fiware_roles.roles.list()
                        if r.name == 'provider')
        for user in users:
            keystone.fiware_roles.roles.add_to_user(
                role=provider_role,
                user=user,
                application=idm_app,
                organization=user.default_project_id)

instance = PopulateTask()


def _register_user(keystone, name, activate=True):
    email = name + '@test.com'
    user = keystone.user_registration.users.register_user(
        name=email,
        password='test',
        username=name,
        domain=settings.KEYSTONE_DEFAULT_DOMAIN)
    if activate:
        user = keystone.user_registration.users.activate_user(
            user=user.id,
            activation_key=user.activation_key)
    return user

@task
def test_data(keystone_path=settings.KEYSTONE_ROOT, keystone=None):
    """Populate the database with some users, organizations and applications
    for convenience"""

    if not keystone:
        # Log as idm
        config = ConfigParser.ConfigParser()
        config.read(keystone_path + 'etc/keystone.conf')
        admin_port = config.get('DEFAULT', 'admin_port')
        endpoint = 'http://{ip}:{port}/v3'.format(ip='127.0.0.1',
                                                  port=admin_port)
        keystone = client.Client(
            username=settings.IDM_USER_CREDENTIALS['username'],
            password=settings.IDM_USER_CREDENTIALS['password'],
            project_name=settings.IDM_USER_CREDENTIALS['project'],
            auth_url=endpoint)

    # Create some default apps to test
    for app_name in settings.FIWARE_DEFAULT_APPS:
        app = keystone.oauth2.consumers.create(
                app_name, 
                description='Default app in FIWARE',
                grant_type='authorization_code', 
                client_type='confidential')

    owner_role = keystone.roles.find(name='owner')

    # Create 4 users
    users = []
    for i in range(20):
        username = 'us' + ''.join(
            random.choice(string.ascii_lowercase) for i in range(1))
        if i == 0 or i == 1:
            username = 'user'
        users.append(_register_user(keystone, username + str(i)))

    # Log as user0
    user0 = users[0]
    keystone = client.Client(username=user0.name,
                             password='test',
                             project_name=user0.username,
                             auth_url=endpoint)

    # Create 1 organization for user0 and give him owner role in it
    test_org = keystone.projects.create(
        name='Test Organization',
        description='Testing data',
        domain=settings.KEYSTONE_DEFAULT_DOMAIN,
        enabled=True,
        img='/static/dashboard/img/logos/small/group.png',
        city='',
        email='',
        website='')
    keystone.roles.grant(user=user0.id,
                         role=owner_role.id,
                         project=test_org.id)

    # Create 1 application for user0 and give him the provider role
    test_app = keystone.oauth2.consumers.create(
        name='Test Application',
        redirect_uris=['localhost/login'],
        description='Test data',
        scopes=['all_info'],
        client_type='confidential',
        grant_type='authorization_code',
        url='localhost',
        img='/static/dashboard/img/logos/small/app.png')
    provider_role = next(r for r
                         in keystone.fiware_roles.roles.list()
                         if r.name == 'provider')

    keystone.fiware_roles.roles.add_to_user(
        role=provider_role.id,
        user=user0.id,
        application=test_app.id,
        organization=user0.default_project_id)

    # Create a role for the application
    test_role = keystone.fiware_roles.roles.create(
        name='Test role',
        is_internal=False,
        application=test_app.id)

    # Give it the permission to get and assign only the owned roles
    internal_permission_owned = next(
        p for p in keystone.fiware_roles.permissions.list()
        if p.name == settings.INTERNAL_PERMISSIONS[4])
    keystone.fiware_roles.permissions.add_to_role(
        role=test_role,
        permission=internal_permission_owned)

    # And assign the role to user1
    user1 = users[1]
    keystone.fiware_roles.roles.add_to_user(
        role=test_role.id,
        user=user1.id,
        application=test_app.id,
        organization=user1.default_project_id)