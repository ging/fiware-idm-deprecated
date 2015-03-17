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

import uuid

from conf import settings

import keystone as deployment_keystone


def populate(keystone_path, internal_address, public_address,
             admin_address):
    config = deployment_keystone.get_config(keystone_path)
    keystone = deployment_keystone.admin_token_connection(config)

    # Keystone services
    deployment_keystone.create_endpoints(keystone, internal_address, public_address,
        admin_address, config)

    keystone_roles = deployment_keystone.create_keystone_roles(keystone)

    idm_user = deployment_keystone.create_idm_user_and_project(keystone, keystone_roles)
    
    # user our migration method here to asign ids to roles and permissions
    idm_app = create_internal_roles_and_permissions(keystone)

    # Make the idm user administrator
    deployment_keystone.grant_administrator(keystone, idm_app, [idm_user])
    

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

    print ('Created default fiware roles and permissions.')
    return idm_app