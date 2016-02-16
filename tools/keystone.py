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
        return parser

    def take_action(self, parsed_args):
        keystone = _admin_token_connection()
        region = parsed_args.region

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
#         print red('Some errors were encountered:')
#         print red('The following settings couldn\'t be found in your keystone.conf file:')
#         for s in latest_settings:
#             print '\t'+red(s)
#         print red('Please edit the keystone.conf file manually so that it contains the settings above.')
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

# def database_tweak(idm_user, idm_password, common_password='test'):
#     """Tweaks the database setting the same password for all users
#      and the keystone endpoints to localhost. Handy for development or
#      local testing with a production database backup. NEVER USE IN
#      THE PRODUCTION DEPLOYMENT.
#     """
#     warning_message = (
#         'This will ruin your database in a production setting and'
#         ' is a major security issue. Use only for development'
#         ' purposes. Continue? [Y/n]: '
#     )
#     cont = prompt(
#         red(warning_message),
#         default='n',
#         validate='[Y,n]')

#     if cont != 'Y':
#         print red('Cancel tweak')
#         return

#     print 'Proceed...'

#     keystone = _admin_token_connection()

#     print 'Set all users password to a fixed value'
#     for user in keystone.users.list():
#         keystone.users.update(user, password=common_password)

#     print 'Set the idm user password to the configured one'
#     idm = keystone.users.find(name=idm_user)
#     keystone.users.update(idm, password=idm_password)

#     print 'tweak the identity service endpoints to point to a development keystone'
#     identity_service = next(s for s in keystone.services.list() if s.type == 'identity')
#     identity_endpoints = [
#         e for e in keystone.endpoints.list()
#         if e.service_id == identity_service.id
#     ]
#     for endpoint in identity_endpoints:
#         keystone.endpoints.update(
#             endpoint,
#             url=('http://{address}/{api_version}'.format(
#                 address=os.environ.get('OS_SERVICE_ENDPOINT'),
#                 api_version=os.environ.get('OS_IDENTITY_API_VERSION')))
#         )

#     print 'Tweak Succesfull'
