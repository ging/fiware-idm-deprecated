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

from collections import namedtuple

from deployment.conf import settings

from fabric.api import run
from fabric.context_managers import cd
from fabric.contrib import console

from keystoneclient.v3 import client

def deploy(dev):
    """Fully installs the IdM backend"""
    # TODO(garcianavalon) PARAMETERS!!!
    install(dev=dev)
    database_create()
    if not dev:
        service_create()
        service_start()
        database_init()
    if dev:
        print 'Run fab keystone_dev_server on another terminal to \
            run keystone\'s dev server'
        if console.confirm("Do you want to install now the initial data?"):
            database_init()
        else:
            print 'Run fab keystone_database_init when you are ready.'

        if console.confirm("Do you want to install now some test data?"):
            test_data()
        else:
            print 'Run fab keystone_database_test_data when you are ready.'

def install(keystone_path, dev):
    print 'Installing backend (Keystone)'
    if os.path.isdir(keystone_path[:-1]):
        print 'already downloaded'
    else:
        run('git clone https://github.com/ging/keystone.git \
            {0}'.format(keystone_path))
    # run('sudo apt-get install python-dev libxml2-dev \
    #         libxslt1-dev libsasl2-dev libsqlite3-dev libssl-dev \
    #         libldap2-dev libffi-dev')
    with cd(keystone_path):
        if dev:
            run('git checkout development')
        run('sudo python tools/install_venv.py')
        run('sudo cp etc/keystone.conf.sample etc/keystone.conf')
        # Uncomment config file
        with cd('etc/'):
            run("sudo sed -i 's/#admin_token/admin_token/g' keystone.conf")
            run("sudo sed -i 's/#admin_port/admin_port/g' keystone.conf")
            run("sudo sed -i 's/#public_port/public_port/g' keystone.conf")
    print 'Done!'

def database_create(keystone_path, verbose):
    add_verbose = '-v' if verbose else ''
    with cd(keystone_path):
        run('sudo tools/with_venv.sh bin/keystone-manage {v} db_sync'.format(
            v=add_verbose))
        run('sudo tools/with_venv.sh bin/keystone-manage {v} db_sync \
            --extension=oauth2'.format(v=add_verbose))
        run('sudo tools/with_venv.sh bin/keystone-manage {v} db_sync \
            --extension=roles'.format(v=add_verbose))
        run('sudo tools/with_venv.sh bin/keystone-manage {v} db_sync \
            --extension=user_registration'.format(v=add_verbose))

def service_create(absolute_keystone_path):
    in_file = open('keystone_idm.conf')
    src = string.Template(in_file.read())
    out_file = open("tmp_keystone_idm.conf", "w")
    out_file.write(src.substitute({
        'absolute_keystone_path': absolute_keystone_path}))
    out_file.close()
    run('sudo cp tmp_keystone_idm.conf /etc/init/keystone_idm.conf')
    run('sudo rm tmp_keystone_idm.conf')

def service_start():
    run('sudo service keystone_idm start')

def service_stop():
    run('sudo service keystone_idm stop')

def dev_server(keystone_path):
    """Runs the server in dev mode."""
    with cd(keystone_path):
        run('sudo tools/with_venv.sh bin/keystone-all -v')

def database_delete(db_path):
    if os.path.isfile(db_path):
        run('sudo rm ' + db_path)

def create_endpoints(keystone, internal_address, public_address,
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

def admin_token_connection(config):
    
    admin_port = config.get('DEFAULT', 'admin_port')
    token = config.get('DEFAULT', 'admin_token')

    endpoint = 'http://{ip}:{port}/v3'.format(ip='127.0.0.1',
                                              port=admin_port)
    keystone = client.Client(token=token, endpoint=endpoint)
    print 'Connected to keystone using token'

    return keystone

def get_config(keystone_path):
    config = ConfigParser.ConfigParser()
    config.read(keystone_path + 'etc/keystone.conf')
    return config

def create_keystone_roles(keystone):
    # Default keystone roles
    # NOTE(garcianavalon) don't confuse it with keystone v2 API
    # default role (member_role_name=_member_). We need a default
    # role to add users to projects. Horizon knows this role throught
    # the local_settings.py file.
    keystone_roles = {
        'member': keystone.roles.create(name='member'),
        'owner': keystone.roles.create(name='owner'),
        'admin': keystone.roles.create(name='admin'),
    }
    print 'created default keystone roles'
    return keystone_roles

def create_idm_user_and_project(keystone, keystone_roles):
    idm_project = keystone.projects.create(
        name=settings.IDM_USER_CREDENTIALS['project'],
        description='',
        is_default=True,
        domain=settings.IDM_USER_CREDENTIALS['domain'])

    idm_user = keystone.users.create(
        name=settings.IDM_USER_CREDENTIALS['username'],
        username=settings.IDM_USER_CREDENTIALS['username'],
        password=settings.IDM_USER_CREDENTIALS['password'],
        default_project=idm_project,
        domain=settings.IDM_USER_CREDENTIALS['domain'])

    keystone.roles.grant(user=idm_user,
                         role=keystone_roles['admin'],
                         project=idm_project)
    keystone.roles.grant(user=idm_user,
                         role=keystone_roles['owner'],
                         project=idm_project)
    print 'Created default idm project and user.'

    return idm_user

def create_internal_roles_and_permissions(keystone):
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

def grant_administrator(keystone, idm_app, users):
    provider_role = next(r for r
                    in keystone.fiware_roles.roles.list()
                    if r.name == 'provider')
    for user in users:
        keystone.fiware_roles.roles.add_to_user(
            role=provider_role,
            user=user,
            application=idm_app,
            organization=user.default_project_id)

def database_populate(keystone_path, internal_address, public_address,
                  admin_address):

    config = get_config(keystone_path)
    keystone = admin_token_connection(config)

    # Keystone services
    create_endpoints(keystone, internal_address, public_address,
        admin_address, config)

    keystone_roles = create_keystone_roles(keystone)

    idm_user = create_idm_user_and_project(keystone, keystone_roles)
    
    idm_app = create_internal_roles_and_permissions(keystone)

    # Make the idm user administrator
    grant_administrator(keystone, idm_app, [idm_user])


def _register_user(keystone, name, activate=True):
    email = name + '@test.com'
    user = keystone.user_registration.users.register_user(
        name=email,
        password='test',
        username=name,
        domain='default')
    if activate:
        user = keystone.user_registration.users.activate_user(
            user=user.id,
            activation_key=user.activation_key)
    return user

def test_data(keystone_path, keystone=None):
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

    owner_role = keystone.roles.find(name='owner')

    # Create 4 users
    users = []
    for i in range(4):
        users.append(_register_user(keystone, 'user' + str(i)))

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
        domain='default',
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
