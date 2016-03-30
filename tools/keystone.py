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

import code
import logging
import json
import os
import sys
import readline
import rlcompleter

from cliff.command import Command
from keystoneclient.v3 import client


def _admin_token_connection():
    """Connect to keystone using the ADMIN_TOKEN.
    Returns a keystoneclient object.
    """
    keystone = client.Client(
        token=os.environ.get('OS_SERVICE_TOKEN'),
        endpoint=os.environ.get('OS_SERVICE_ENDPOINT'))

    return keystone


class Console(Command):
    """Opens an interactive python console with a connection to Keystone using
    the ADMIN_TOKEN.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        keystone = _admin_token_connection()
        vars = globals()
        vars.update(locals())
        readline.set_completer(rlcompleter.Completer(vars).complete)
        readline.parse_and_bind("tab: complete")
        shell = code.InteractiveConsole(vars)
        shell.interact()

class DeleteRegionAndEndpoints(Command):
    """Deletes a region and all its associated endpoints and endpoint_groups."""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(DeleteRegionAndEndpoints, self).get_parser(prog_name)
        parser.add_argument('region', metavar='region', type=str, nargs='?',
                   help='the region id')
        parser.add_argument('--delete_users', metavar='delete_users', type=bool, nargs='?',
            help='Also delete the region service and admin users.')
        return parser

    def take_action(self, parsed_args):
        keystone = _admin_token_connection()
        region = parsed_args.region
        delete_users = parsed_args.delete_users

        # check region exists
        try:
            keystone.regions.get(region)
        except Exception, e:
            self.log.error('Aborting')
            raise e

        # delete all region endpoints
        for endpoint in keystone.endpoints.list():
            if endpoint.region == region:
                keystone.endpoints.delete(endpoint)
                self.log.info('Deleted endpoint %s', endpoint.id)

        # delete all endpoint groups that filter for region
        for endpoint_group in keystone.endpoint_groups.list():
            if endpoint_group.filters.get('region_id', None) == region:
                keystone.endpoint_groups.delete(endpoint_group)
                self.log.info('Deleted endpoint group %s', endpoint_group.id)

        if delete_users:
            # delete all related users
            projects = [keystone.projects.find(name=p_name).id for p_name in ['admin', 'service',]]
            assignments = []
            for p_id in projects:
                assignments += keystone.role_assignments.list(project=p_id)

            potential_users = [
                (ass.user['id'], keystone.users.get(ass.user['id']).name) for ass in assignments
            ]

            region_slug = region.lower()
            deleted = []
            for (user_id, user_name) in potential_users:
                if user_id in deleted:
                    continue
                if region_slug == user_name.split('-')[-1]:
                    keystone.users.delete(user_id)
                    self.log.info('Deleted user %s with name %s', user_id, user_name)
                    deleted.append(user_id)

        # delete region
        keystone.regions.delete(region)
        self.log.info('Deleted region %s', region)

        # notify user to remember to delete regions in Horizon
        self.log.warning('Remember to delete this region as an available region in Horizon settings!')
        self.log.info('Done :)')

class CancelAccounts(Command):
    """Cancels the account of some users"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CancelAccounts, self).get_parser(prog_name)
        parser.add_argument('users', metavar='users', type=str, nargs='+', help='the users IDs')
        parser.add_argument('-o', '--keystone_owner_role', metavar='keystone_owner_role', type=str, nargs=1, default='owner', help='owner role ID in Keystone')
        parser.add_argument('-p', '--provider_role', metavar='provider_role', type=str, nargs=1, default='provider', help='provider FIWARE role ID')
        return parser

    def take_action(self, parsed_args):
        keystone = _admin_token_connection()

        for user_id in parsed_args.users:
            self.log.info('Deleting user ' + user_id)
            user = keystone.users.get(user_id)
            delete_orgs = self._get_orgs_to_delete(keystone, user, parsed_args.keystone_owner_role)
            delete_apps = self._get_apps_to_delete(keystone, user, parsed_args.provider_role)

            for org_id in delete_orgs:
                self.log.info('Deleting project ' + org_id)
                keystone.projects.delete(org_id)

            for app_id in delete_apps:
                self.log.info('Deleting app ' + app_id)
                keystone.oauth2.consumers.delete(app_id)

            # finally delete the user
            keystone.users.delete(user.id)

        self.log.info('Done :)')

    def _get_orgs_to_delete(self, keystone, user, keystone_owner_role):
        # all orgs where the user is the only owner
        # and user specific organizations
        delete_orgs = [
            user.default_project_id,
            user.cloud_project_id
        ]
        owner_role = keystone.roles.find(name=keystone_owner_role)
        # NOTE(garcianavalon) the organizations the user is owner
        # are already in the request object by the middleware
        for org in keystone.projects.list():
            if org.id in delete_orgs:
                continue

            owners = set([
                a.user['id'] for a
                in keystone.role_assignments.list(role=owner_role.id, project=org.id)
                if hasattr(a, 'user')
            ])

            if len(owners) == 1 and user.id in owners:
                import pdb; pdb.set_trace()
                self.log.info('Org to delete: ' + org.id)
                delete_orgs.append(org.id)

        return delete_orgs

    def _get_apps_to_delete(self, keystone, user, provider_role):
        # all the apps where the user is the only provider
        delete_apps = []
        provider_role = keystone.fiware_roles.roles.get(provider_role)

        provided_apps = [
            a.application_id for a
            in keystone.fiware_roles.role_assignments.list_user_role_assignments(user=user.id)
            if a.role_id == provider_role.id
        ]

        for app_id in provided_apps:
            providers = set([
                a.user_id for a
                in keystone.fiware_roles.role_assignments.list_user_role_assignments(application=app_id)
                if a.role_id == provider_role.id
            ])

            if len(providers) == 1:
                delete_apps.append(app_id)

        return delete_apps


class CreateNewEndpoints(Command):
    """Reads a a json file with a Keystone catalog sintax and creates all the endpoints in it,
    adding an endpoint group filter for each region if there is not one created already.

    The service associated with the endpoints must be already created.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CreateNewEndpoints, self).get_parser(prog_name)
        parser.add_argument('filename', nargs='?', default='endpoints.json')
        return parser

    def take_action(self, parsed_args):
        f = open(parsed_args.filename)
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


# def check(keystone_path):
#     """Check for missing settings in the settings file."""
#     # returns 1 if everything went OK, 0 otherwise
    
#     print 'Checking Keystone...',
#     path = keystone_path + 'etc/'
#     with open(path+'keystone.conf', 'r') as old_file, open(path+'keystone.conf.sample', 'r') as new_file:
#         old = set(old_file)
#         new = set(new_file)
#     new_settings = set()
#     old_settings = set()

#     for s in new.difference(old):
#         new_settings.add(_parse_setting(s))
#     for s in old.difference(new):
#         old_settings.add(_parse_setting(s))
#     latest_settings = new_settings.difference(old_settings)
#     if not latest_settings:
#         print (green('Everything OK'))
#         return 1 # flag for the main task
#     else:
#         log.warning('Some errors were encountered:')
#         log.warning('The following settings couldn\'t be found in your keystone.conf file:')
#         for s in latest_settings:
#             print '\t'+red(s)
#         log.warning('Please edit the keystone.conf file manually so that it contains the settings above.')
#         return 0 # flag for the main task

# def _parse_setting(setting):
#     if '=' in setting:
#         if '#' in setting:
#             if setting[1] == ' ':
#                 return setting[setting.find('#')+2:setting.find('=')]
#             else:
#                 return setting[setting.find('#')+1:setting.find('=')]
#         else:
#             return setting[0:setting.find('=')]

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

class DatabaseTweak(Command):
    """Tweaks the database setting the same password for all users
    and the keystone endpoints to localhost. Handy for development or
    local testing with a production database backup. NEVER USE IN
    THE PRODUCTION DEPLOYMENT.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(DatabaseTweak, self).get_parser(prog_name)
        parser.add_argument('-np', '--common_password', metavar='common_password', type=str, nargs=1,
        default='test', help='the new password for all users')

        parser.add_argument('-u', '--idm_user', metavar='idm_user', type=str, nargs=1,
        default='idm', help='the username of the horizon admin account')

        parser.add_argument('-p', '--idm_password', metavar='idm_password', type=str, nargs=1,
        default='idm', help='the new password for the horizon admin account')
        return parser

    def take_action(self, parsed_args):
        keystone = _admin_token_connection()
        password = parsed_args.common_password
        idm_user = parsed_args.idm_user
        idm_password = parsed_args.idm_password

        warning_message = (
            'This will ruin your database in a production setting and'
            ' is a major security issue. Use only for development'
            ' purposes. Continue?: '
        )

        cont = query_yes_no(warning_message)

        if not cont:
            self.log.warning('Cancel tweak')
            return

        self.log.info('Proceed...')

        keystone = _admin_token_connection()

        self.log.info('Set all users password to a fixed value')

        for user in keystone.users.list():
            keystone.users.update(user, password=password)

        self.log.info('Set the idm user password to the configured one')

        idm = keystone.users.find(name=idm_user)
        keystone.users.update(idm, password=idm_password)

        self.log.info('tweak the identity service endpoints to point to a development keystone')

        identity_service = next(s for s in keystone.services.list() if s.type == 'identity')
        identity_endpoints = [
            e for e in keystone.endpoints.list()
            if e.service_id == identity_service.id
        ]
        url = os.environ.get('OS_SERVICE_ENDPOINT')

        for endpoint in identity_endpoints:
            keystone.endpoints.update(endpoint, url=url)

        self.log.info('Tweak Succesfull')
