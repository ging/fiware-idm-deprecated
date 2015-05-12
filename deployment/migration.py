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

import datetime
import json
import os
import uuid

from deployment.keystone import PopulateTask
from conf import settings

from keystoneclient import exceptions


# This dictinary holds the old ids for permissions and roles. Only used
# for migration purposes.
MIGRATION_OLD_IDS = {
    'Manage the application': '5',
    'Manage roles': '6',
    'Get and assign all public application roles': '7',
    'Manage Authorizations': '8',
    'provider': '285',
    'purchaser': '6453fc41aa9d404b984d9da0566a1f7e',
}

CLOUD_APP_ID = 'f8999e1ee0884195997b63280c2b0264'
CLOUD_ROLE_ID = 'd38d9cd4fa524b87a87feb45904480f7'

NO_FILTER_ENDPOINT_GROUP_ID = '628912b79e5540b8a08d33e5eb60c233'

class MigratePopulateTask(PopulateTask):
    """Populates the database with migration specifics from the old idm."""
    name = "populate"
    def run(self, keystone_path=settings.KEYSTONE_ROOT):
        keystone = self._admin_token_connection()
	# migration old ids not configured
	raise Exception()
        # Keystone services
        self._create_services_and_endpoints(keystone)
        # Enpoint groups
        self._create_endpoint_group_filters(keystone)

        keystone_roles = self._create_keystone_roles(keystone)

        idm_user = self._create_idm_user_and_project(keystone, keystone_roles)
        
        # user our migration method here to asign ids to roles and permissions
        idm_app = self._create_internal_roles_and_permissions(keystone)

        # Make the idm user administrator
        self._grant_administrator(keystone, idm_app, [idm_user])

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


class MigrateCategoriesTask(PopulateTask):
    """Assignates a category to the old users."""
    name = "user_categories"

    def run(self, keystone_path=settings.KEYSTONE_ROOT):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        categories = json.load(open(os.path.join(__location__, 'categories.json')))

        keystone = self._admin_token_connection()

        self.trial_role = keystone.roles.find(name='trial')
        self.community_role = keystone.roles.find(name='community')
        self.basic_role = keystone.roles.find(name='basic')

        for data in categories:
            user_id = data['user_id']
            role_id = data['role_id']
            region_id = data.get('region_id', None)

            if (role_id == self.trial_role.id
                and not region_id):

                region_id = 'Spain2'

            if role_id == self.community_role.id and not region_id:

                print ('ERROR: {0} community with no region'.format(user_id))
                continue

            if role_id == self.basic_role.id and region_id:

                region_id = None
                
                print ('WARNING: {0} basic with region, ignoring it'.format(user_id))

            if role_id not in [self.trial_role.id, self.basic_role.id, self.community_role.id]:
                print ('ERROR: {0} invalid role_id {1}'.format(user_id, role_id))
                continue

            self.update_account(keystone, user_id, role_id, region_id)


    def update_account(self, keystone, user_id, role_id, region_id=None):
        user = keystone.users.get(user_id)

        # grant the selected role
        keystone.roles.grant(user=user_id, role=role_id, domain='default')

        date = str(datetime.date.today())
        if role_id == self.trial_role.id:

            keystone.users.update(user=user, trial_started_at=date)
        elif role_id == self.community_role.id:
            keystone.users.update(user=user, community_started_at=date)

        # cloud
        if role_id != self.basic_role.id:
            self._activate_cloud(keystone, user_id, user.cloud_project_id)
        
        # assign endpoint group for the selected region
        if not region_id:
            return

        endpoint_groups = keystone.endpoint_groups.list()
        region_group = next(group for group in endpoint_groups
            if group.filters.get('region_id', None) == region_id)

        if not region_group:
            print ('There is no endpoint group defined for {0}'.format(region_id))
        
        keystone.endpoint_groups.add_endpoint_group_to_project(
            project=user.cloud_project_id,
            endpoint_group=region_group)

        # done!
        print ('OK: {0}'.format(user_id))

    def _activate_cloud(self, keystone, user_id, cloud_project_id):
        # grant purchaser in cloud app to cloud org
        # and Member to the user

        keystone.fiware_roles.roles.add_to_organization(
            role=MIGRATION_OLD_IDS['purchaser'],
            organization=cloud_project_id,
            application=CLOUD_APP_ID)

        keystone.fiware_roles.roles.add_to_user(
            role=CLOUD_ROLE_ID,
            user=user_id,
            organization=cloud_project_id,
            application=CLOUD_APP_ID)


instance2 = MigrateCategoriesTask()


class AllRegionsForAllUsersTask(PopulateTask):
    """Assignates the no-filter endpoint group to all users"""
    name = "all_regions_to_all_users"

    def run(self, keystone_path=settings.KEYSTONE_ROOT):
        keystone = self._admin_token_connection()

        all_users = keystone.users.list()

        for user in all_users:
            if not hasattr(user, 'cloud_project_id'):
                print 'Skip {0}, no cloud project id'.format(user.name)
                continue
            try:
                keystone.endpoint_groups.add_endpoint_group_to_project(
                    project=user.cloud_project_id,
                    endpoint_group=NO_FILTER_ENDPOINT_GROUP_ID)

                print '200 OK {0}'.format(user.name)
            except exceptions.Conflict:
                print '409 User {0} already has it'.format(user.name)
            except exceptions.NotFound:
                print '404 Not found project {0} for user {1}'.format(
                    user.cloud_project_id, user.name)

        print 'Done.'


instance3 = AllRegionsForAllUsersTask()


class AssignDefaultProjectTask(PopulateTask):
    """Assigns a default project to a list of users defined in a file."""
    name = "default_project_to_admins"

    def run(self, keystone_path=settings.KEYSTONE_ROOT):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        admins = json.load(open(os.path.join(__location__, 'keystone_admins.json')))

        keystone = self._admin_token_connection()

        admin_project = keystone.projects.find(name='admin')
        import pdb; pdb.set_trace()

        for user_name in admins:
            user = keystone.users.find(name=user_name)
            res = keystone.users.update(user, default_project=admin_project)
            print user_name, res
        

        print 'Done.'


instance4 = AssignDefaultProjectTask()


class SetNameAsUsernameTask(PopulateTask):
    """Sets username to name to a list of users defined in a file."""
    name = "set_username"

    def run(self, users_file):
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        admins = json.load(open(os.path.join(__location__, users_file)))

        keystone = self._admin_token_connection()

        for user_name in admins:
            user = keystone.users.find(name=user_name)
            res = keystone.users.update(user, username=user_name)
            print user_name, res
        

        print 'Done.'


instance5 = SetNameAsUsernameTask()
