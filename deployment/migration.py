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

from deployment.keystone import PopulateTask
from conf import settings


# This dictinary holds the old ids for permissions and roles. Only used
# for migration purposes.
MIGRATION_OLD_IDS = {
    'Manage the application': '4',
    'Manage roles': '5',
    'Get and assign all application roles': '8',
    'Manage Authorizations': '6',
    'provider': '106',
    'purchaser': '191',
}

class MigratePopulateTask(PopulateTask):
    """Populates the database with migration specifics from the old idm."""
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
        
        # user our migration method here to asign ids to roles and permissions
        idm_app = self._create_internal_roles_and_permissions(keystone)

        # Make the idm user administrator
        self._grant_administrator(keystone, idm_app, [idm_user])

    def _create_internal_roles_and_permissions(keystone):
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
            old_id = MIGRATION_OLD_IDS.get(permission, uuid.uuid4().hex)
            created_permissions.append(
                keystone.fiware_roles.permissions.create(
                    id=old_id, name=permission, application=idm_app, is_internal=True))
        
        created_roles = []
        for role in settings.INTERNAL_ROLES:
            old_id = MIGRATION_OLD_IDS.get(role, uuid.uuid4().hex)
            created_role = keystone.fiware_roles.roles.create(
                id=old_id, name=role, application=idm_app, is_internal=True)
            created_roles.append(created_role)
            # Link roles with permissions
            for index in settings.INTERNAL_ROLES[role]:
                keystone.fiware_roles.permissions.add_to_role(
                    created_role, created_permissions[index])

        print ('Created default fiware roles and permissions.')
        return idm_app

instance = MigratePopulateTask()