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

IDM_ROOT = './'
KEYSTONE_ROOT = IDM_ROOT + 'keystone/'
HORIZON_ROOT = IDM_ROOT + 'horizon/'
FIWARECLIENT_ROOT = IDM_ROOT + 'fiwareclient/'

# Hosts
HOSTS = {
    'keystone': ['138.4.4.131'],
    'horizon': ['138.4.4.131'],
}

# Development settings
KEYSTONE_DEV_DATABASE = 'keystone.db'
HORIZON_DEV_ADDRESS = '127.0.0.1:8000'

# TODO(garcianavalon) sync this with the extension,
# see https://trello.com/c/rTsUMnjw
INTERNAL_ROLES = {
    'provider': [0, 1, 2, 3, 4],
    'purchaser': [3],
}
INTERNAL_PERMISSIONS = [
    'Manage the application',
    'Manage roles',
    'Get and assign all application roles',
    'Manage Authorizations',
    'Get and assign only owned roles',
]

IDM_USER_CREDENTIALS = {
    'username': 'idm',
    'password': 'idm',
    'project': 'idm',
    'domain': 'default',
}

CONTROLLER_PUBLIC_ADDRESS = '127.0.0.1'
CONTROLLER_ADMIN_ADDRESS = '127.0.0.1'
CONTROLLER_INTERNAL_ADDRESS = '127.0.0.1'

# TODO(garcianavalon): split dependencies
UBUNTU_DEPENDENCIES = {
	'install_command': 'sudo apt-get install',
	'horizon': [
		'python-dev',
		'python-virtualenv',
		'libxml2-dev',
		'libxslt1-dev',
		'libsasl2-dev',
		'libsqlite3-dev',
		'libssl-dev',
		'libldap2-dev',
		'libffi-dev',
		'libjpeg8-dev',
	],
    'keystone': [
    ],
    'mysql': [
    ],
    'sqlite': [
    ],
}

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
