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
import json
import os
import string

from conf import settings

from keystoneclient.v3 import client

from fabric.api import task
from fabric.tasks import Task
from fabric.state import env
from fabric.api import execute


@task
def install(keystone_path=settings.KEYSTONE_ROOT):
    """Download and install the Back-end and its dependencies."""
    if env.exists(keystone_path[:-1]):
        print 'Already downloaded.'
    else:
        env.run(('git clone https://github.com/ging/keystone.git '
                 '{0}').format(keystone_path))
    with env.cd(keystone_path):
        dependencies = ' '.join(settings.UBUNTU_DEPENDENCIES['keystone'])
        
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
def database_create(keystone_path=settings.KEYSTONE_ROOT, verbose=True):
    add_verbose = '-v' if verbose else ''
    with env.cd(keystone_path):
        env.run(('sudo tools/with_venv.sh bin/keystone-manage {v}'
            ' db_sync').format(v=add_verbose))
        env.run(('sudo tools/with_venv.sh bin/keystone-manage {v}'
            ' db_sync --extension endpoint_filter').format(v=add_verbose))
        env.run(('sudo tools/with_venv.sh bin/keystone-manage {v}'
            ' db_sync --extension=oauth2').format(v=add_verbose))
        env.run(('sudo tools/with_venv.sh bin/keystone-manage {v}'
            ' db_sync --extension=roles').format(v=add_verbose))
        env.run(('sudo tools/with_venv.sh bin/keystone-manage {v}'
            ' db_sync --extension=user_registration').format(v=add_verbose))

@task
def database_delete(keystone_path=settings.KEYSTONE_ROOT):
    db_path = keystone_path + settings.KEYSTONE_DEV_DATABASE
    if os.path.isfile(db_path):
        env.run('sudo rm ' + db_path)

@task
def database_reset(keystone_path=settings.KEYSTONE_ROOT):
    """Deletes keystone's database and create a new one, populated with
    the base data needed by the IdM. Requires a keystone instance running.
    """
    execute('keystone.database_delete', keystone_path=keystone_path)
    execute('keystone.database_create', keystone_path=keystone_path)
    execute('keystone.populate', keystone_path=keystone_path)


@task
def set_up_as_service(absolute_keystone_path=None):
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
def start():
    """Runs the service."""
    env.run('sudo service keystone_idm start')

@task
def stop():
    """Stops the service."""
    env.run('sudo service keystone_idm stop')

@task
def restart():
    """Restarts the service."""
    env.run('sudo service keystone_idm restart')

@task
def dev_server(keystone_path=settings.KEYSTONE_ROOT):
    """Runs the server in dev mode."""
    with env.cd(keystone_path):
        env.run('sudo tools/with_venv.sh bin/keystone-all -v')

@task
def delete_region_and_endpoints(region):
    """Deletes a region and all its associated endpoints and endpoint_groups."""
    admin_port = settings.KEYSTONE_ADMIN_PORT
    token = settings.KEYSTONE_ADMIN_TOKEN

    endpoint = 'http://{ip}:{port}/v3'.format(ip='127.0.0.1',
                                              port=admin_port)
    keystone = client.Client(token=token, endpoint=endpoint)

    # check region exists
    keystone.regions.get(region)

    # delete all region endpoints
    for endpoint in keystone.endpoints.list():
        if endpoint.region == region:
            keystone.endpoints.delete(endpoint)

    # delete all endpoint groups that filter for region
    for endpoint_group in keystone.endpoint_groups.list():
        if endpoint_group.filters.get('region_id', None) == region:
            keystone.endpoint_groups.delete(endpoint_group)

    # delete region
    keystone.regions.delete(region)

@task
def create_new_endpoints(endpoints_file):
    """Creates all the endpoints in a json file, adding an endpoint group
    filter for each region (if there is not currently one created). The service
    must be already created.
    """
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    f = open(os.path.join(__location__, endpoints_file))
    catalog = json.load(f)

    admin_port = settings.KEYSTONE_ADMIN_PORT
    token = settings.KEYSTONE_ADMIN_TOKEN

    endpoint = 'http://{ip}:{port}/v3'.format(ip='127.0.0.1',
                                              port=admin_port)
    keystone = client.Client(token=token, endpoint=endpoint)

    endpoint_groups = keystone.endpoint_groups.list()
    services = keystone.services.list()

    regions = set()
    for service_data in catalog:
        service = next((s for s in services if s.type == service_data['type']), None)

        if not service:
            print ('Service {0} type {1} is not created,'
                   ' skipping these endpoints').format(service_data['name'],
                                                       service_data['type'])
            continue

        for endpoint in service_data['endpoints']:
            interfaces = [
                ('public', endpoint['publicURL']),
                ('admin', endpoint['adminURL']),
                ('internal', endpoint['internalURL']),
            ]
            for interface, url in interfaces:
                keystone.endpoints.create(
                    region=endpoint['region'],
                    service=service,
                    url=url,
                    interface=interface)
                print 'Created {0} for service {1} and region {2}'.format(
                    url, service, endpoint['region'])

            regions.add(endpoint['region'])

    # create endpoint group for region if it doesnt exists
    for region in regions:

        endpoint_group_for_region = [
            eg for eg in endpoint_groups
            if eg.filters.get('region_id', None) == region
        ]

        if not endpoint_group_for_region:
            print 'Creating endpoint_group for region {0}'.format(region)
            keystone.endpoint_groups.create(
                name=region + ' Region Group',
                filters={
                    'region_id': region
                })


class PopulateTask(Task):
    name = "populate"
    def run(self, keystone_path=settings.KEYSTONE_ROOT):
        keystone = self._admin_token_connection()

        # Keystone services
        self._create_services_and_endpoints(keystone)
        # Enpoint groups
        self._create_endpoint_group_filters(keystone)

        keystone_roles = self._create_keystone_roles(keystone)

        idm_user = self._create_idm_user_and_project(keystone, keystone_roles)

        idm_app = self._create_internal_roles_and_permissions(keystone)

        # Make the idm user administrator
        self._grant_administrator(keystone, idm_app, [idm_user])

    def _create_services_and_endpoints(self, keystone):
        for service_data in settings.SERVICE_CATALOG:
            service = keystone.services.create(
                name=service_data['name'],
                type=service_data['type'],
                description=service_data.get('description', None))

            for endpoint in service_data['endpoints']:
                interfaces = [
                    ('public', endpoint['publicURL']),
                    ('admin', endpoint['adminURL']),
                    ('internal', endpoint['internalURL']),
                ]
                for interface, url in interfaces:
                    keystone.endpoints.create(
                        region=endpoint['region'],
                        service=service,
                        url=url,
                        interface=interface)

        print 'Created Services and Endpoints'

    def _create_endpoint_group_filters(self, keystone):
        """Create an endpoint group that filters for each region and one
        that filters for identity service.
        """
        regions = keystone.regions.list()
        for region in regions:
            keystone.endpoint_groups.create(
                name=region.id + ' Region Group',
                filters={
                    'region_id': region.id
                })
        identity_services = [service for service 
                             in keystone.services.list(type='identity')
                             if service.type == 'identity']

        for service in identity_services:
            keystone.endpoint_groups.create(
                name=service.name + ' Identity Group',
                filters={
                    'service_id': service.id
                })

    def _admin_token_connection(self):
        admin_port = settings.KEYSTONE_ADMIN_PORT
        token = settings.KEYSTONE_ADMIN_TOKEN

        endpoint = 'http://{ip}:{port}/v3'.format(ip='127.0.0.1',
                                                  port=admin_port)
        keystone = client.Client(token=token, endpoint=endpoint)

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
            'trial': keystone.roles.create(name='trial', is_default=True),
            'basic': keystone.roles.create(name='basic', is_default=True),
            'community': keystone.roles.create(name='community', is_default=True),
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

        print 'Created default fiware roles and permissions.'
        return idm_app

    def _grant_administrator(self, keystone, idm_app, users):
        provider_role = next(
            r for r in keystone.fiware_roles.roles.list()
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
def test_data(keystone_path=settings.KEYSTONE_ROOT):
    """Populate the database with some users, organizations and applications
    for convenience"""

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
        # Create default roles
        for role_name in settings.FIWARE_DEFAULT_APPS[app_name]:
            keystone.fiware_roles.roles.create(
                name=role_name,
                is_internal=False,
                application=app.id)

    owner_role = keystone.roles.find(name='owner')

    # Create 4 users
    users = []
    for i in range(10):
        username = 'user'
        users.append(_register_user(keystone, username + str(i)))

    # Log as user0
    user0 = users[0]

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
