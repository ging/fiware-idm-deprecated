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
import code
import readline
import rlcompleter

from conf import settings

from keystoneclient.v3 import client

from fabric.api import task
from fabric.operations import prompt
from fabric.colors import red, green


@task
def console():
    """Opens an interactive python console with a connection to Keystone using 
    the ADMIN_TOKEN.
    """
    keystone = _admin_token_connection()

    vars = globals()
    vars.update(locals())
    readline.set_completer(rlcompleter.Completer(vars).complete)
    readline.parse_and_bind("tab: complete")
    shell = code.InteractiveConsole(vars)
    shell.interact()

@task
def check(keystone_path=settings.KEYSTONE_ROOT):
    """Check for missing settings in the settings file."""
    # returns 1 if everything went OK, 0 otherwise
    
    print 'Checking Keystone...',
    path = keystone_path + 'etc/'
    with open(path+'keystone.conf', 'r') as old_file, open(path+'keystone.conf.sample', 'r') as new_file:
        old = set(old_file)
        new = set(new_file)
    new_settings = set()
    old_settings = set()

    for s in new.difference(old):
        new_settings.add(_parse_setting(s))
    for s in old.difference(new):
        old_settings.add(_parse_setting(s))
    latest_settings = new_settings.difference(old_settings)
    if not latest_settings:
        print (green('Everything OK'))
        return 1 # flag for the main task
    else:
        print red('Some errors were encountered:')
        print red('The following settings couldn\'t be found in your keystone.conf file:')
        for s in latest_settings:
            print '\t'+red(s)
        print red('Please edit the keystone.conf file manually so that it contains the settings above.')
        return 0 # flag for the main task

def _parse_setting(setting):
    if '=' in setting:
        if '#' in setting:
            if setting[1] == ' ':
                return setting[setting.find('#')+2:setting.find('=')]
            else:
                return setting[setting.find('#')+1:setting.find('=')]
        else:
            return setting[0:setting.find('=')]

@task
def database_tweak(keystone_address, keystone_port, common_password='test'):
    """Tweaks the database setting the same password for all users
     and the keystone endpoints to localhost. Handy for development or
     local testing with a production database backup. NEVER USE IN
     THE PRODUCTION DEPLOYMENT.
    """
    warning_message = (
        'This will ruin your database in a production setting and'
        ' is a major security issue. Use only for development'
        ' purposes. Continue? [Y/n]: '
    )
    cont = prompt(
        red(warning_message),
        default='n',
        validate='[Y,n]')

    if cont != 'Y':
        print red('Cancel tweak')
        return

    print 'Proceed...'

    keystone = _admin_token_connection()

    print 'Set all users password to a fixed value'
    for user in keystone.users.list():
        keystone.users.update(user, password=common_password)

    print 'Set the idm user password to the configured one'
    idm = keystone.users.find(name=settings.IDM_USER_CREDENTIALS['username'])
    keystone.users.update(idm, password=settings.IDM_USER_CREDENTIALS['password'])

    print 'tweak the identity service endpoints to point to a development keystone'
    identity_service = next(s for s in keystone.services.list() if s.type == 'identity')
    identity_endpoints = [
        e for e in keystone.endpoints.list()
        if e.service_id == identity_service.id
    ]
    for endpoint in identity_endpoints:
        keystone.endpoints.update(
            endpoint,
            url=('http://{ip}:{port}/v3').format(
                ip=keystone_address,
                port=keystone_port
            )
        )

    print 'Tweak Succesfull'


@task
def delete_region_and_endpoints(region):
    """Deletes a region and all its associated endpoints and endpoint_groups."""
    keystone = _admin_token_connection()

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

    keystone = _admin_token_connection()

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
                    url, service.id, endpoint['region'])

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

def _admin_token_connection():
    admin_port = settings.KEYSTONE_ADMIN_PORT
    token = settings.KEYSTONE_ADMIN_TOKEN

    endpoint = 'http://{ip}:{port}/v3'.format(ip='127.0.0.1',
                                              port=admin_port)
    keystone = client.Client(token=token, endpoint=endpoint)

    return keystone


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
