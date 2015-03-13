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
import uuid

from conf import settings

import keystone as deployment_keystone

from keystoneclient.v3 import client


def populate(keystone_path, internal_address, public_address,
             admin_address):
    config = ConfigParser.ConfigParser()
    config.read(keystone_path + 'etc/keystone.conf')
    admin_port = config.get('DEFAULT', 'admin_port')
    public_port = config.get('DEFAULT', 'public_port')
    token = config.get('DEFAULT', 'admin_token')

    endpoint = 'http://{ip}:{port}/v3'.format(ip='127.0.0.1',
                                              port=admin_port)
    keystone = client.Client(token=token, endpoint=endpoint)
    print 'Connected to keystone using token'

    # Keystone service
    deployment_keystone.create_endpoints(keystone, internal_address,
        public_address, admin_address, public_port)

    # Default keystone roles
    # NOTE(garcianavalon) don't confuse it with keystone v2 API
    # default role (member_role_name=_member_). We need a default
    # role to add users to projects. Horizon knows this role throught
    # the local_settings.py file.
    member_role = keystone.roles.create(name='member')
    admin_role = keystone.roles.create(name='admin')
    print 'created default keystone roles'

    # idm Tenant
    idm_tenant = keystone.projects.create(
        name=settings.IDM_USER_CREDENTIALS['project'],
        description='',
        is_default=True,
        domain=settings.IDM_USER_CREDENTIALS['domain'])

    idm_user = keystone.users.create(
        name=settings.IDM_USER_CREDENTIALS['username'],
        username=settings.IDM_USER_CREDENTIALS['username'],
        password=settings.IDM_USER_CREDENTIALS['password'],
        default_project=idm_tenant,
        domain=settings.IDM_USER_CREDENTIALS['domain'])

    keystone.roles.grant(user=idm_user,
                         role=admin_role,
                         project=idm_tenant)

    print 'Created default idm project and user.'

    # Default internal application
    # Log as idm
    keystone = client.Client(
        username=idm_user.name,
        password=settings.IDM_USER_CREDENTIALS['password'],
        project_name=idm_user.name,
        auth_url=endpoint)

    idm_app = keystone.oauth2.consumers.create(
        settings.IDM_USER_CREDENTIALS['username'], 
        description='',
        grant_type='authorization_code', 
        client_type='confidential', 
        is_default=True)

    # Default Permissions and roles
    created_permissions = []
    for permission in settings.INTERNAL_PERMISSIONS:
        old_id = settings.MIGRATION_OLD_IDS.get(permission, uuid.uuid4().hex)
        created_permissions.append(
            keystone.fiware_roles.permissions.create(
                id=old_id, name=permission, application=idm_app, is_internal=True))
    
    created_roles = []
    for role in settings.INTERNAL_ROLES:
        old_id = settings.MIGRATION_OLD_IDS.get(role, uuid.uuid4().hex)
        created_role = keystone.fiware_roles.roles.create(
            id=old_id, name=role, application=idm_app, is_internal=True)
        created_roles.append(created_role)
        # Link roles with permissions
        for index in settings.INTERNAL_ROLES[role]:
            keystone.fiware_roles.permissions.add_to_role(
                created_role, created_permissions[index])

    # Make the idm user administrator
    provider_role = next(r for r
                    in keystone.fiware_roles.roles.list()
                    if r.name == 'provider')
    keystone.fiware_roles.roles.add_to_user(
        role=provider_role,
        user=idm_user,
        application=idm_app,
        organization=idm_tenant)

    print ('Created default fiware roles and permissions.')