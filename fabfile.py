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
import os
import sys

from collections import namedtuple

from fabric.api import local
from fabric.context_managers import lcd

IDM_ROOT = ''
KEYSTONE_ROOT = IDM_ROOT + 'keystone/'
HORIZON_ROOT = IDM_ROOT + 'horizon/'
FIWARECLIENT_ROOT = IDM_ROOT + 'fiwareclient/'

# TODO(garcianavalon) sync this with the extension, see https://trello.com/c/rTsUMnjw
INTERNAL_ROLES = {
	'provider':[0, 1, 2, 3, 4],
	'purchaser':[3],
}
INTERNAL_PERMISSIONS = [
	'Manage the application',
	'Manage roles', 
	'Get and assign all application roles',
	'Manage Authorizations',
	'Get and assign only owned roles',
]
CONTROLLER_PUBLIC_ADDRESS = '127.0.0.1'
CONTROLLER_ADMIN_ADDRESS = '127.0.0.1'
CONTROLLER_INTERNAL_ADDRESS = '127.0.0.1'


def deploy(dev=False):
	"""Fully installs the IdM."""
	# TODO(garcianavalon) PARAMETERS!!!
	fiwareclient_install()
	keystone_deploy(dev=dev)
	horizon_deploy(dev=dev)
	print 'IdM successfully deployed! :)'

def fiwareclient_install(fiwareclient_path=FIWARECLIENT_ROOT):
	""" Download and install locally the fiwareclient."""
	print 'Installing the custom keystoneclient aka fiwareclient'
	local('git clone https://github.com/ging/python-keystoneclient \
		{0}'.format(fiwareclient_path))
	print 'Done!'

def _fiwareclient_check_installation(fiwareclient_path=FIWARECLIENT_ROOT):
	"""Check if fiwareclient has been correctly set up"""
	# NOTE(garcianavalon) add the fiwareclient to PYTHONPATH
	sys.path.insert(1, fiwareclient_path)
	try:
		from keystoneclient.v3 import client
		return client
	except Exception, e:
		# TODO(garcianavalon) custom message/exception
		raise e
	
# HORIZON
def horizon_deploy(dev=False):
	"""Fully installs the IdM frontend"""
	# TODO(garcianavalon) PARAMETERS!!!
	horizon_install()
	if dev:
		horizon_dev_runserver()
	else:
		# TODO(garcianavalon) production server!
		pass



def horizon_install(horizon_path=HORIZON_ROOT, 
					fiwareclient_path=FIWARECLIENT_ROOT):
	"""Download and install Horizon and its dependencies."""
	print 'Installing frontend (Horizon)'
	local('sudo apt-get install git python-dev python-virtualenv \
		libssl-dev libffi-dev libjpeg8-dev')
	if os.path.isdir(horizon_path[:-1]):

		print 'already downloaded'
	else:
		local('git clone https://github.com/ging/horizon.git {0}'.format(horizon_path))
	# NOTE(garcianavalon) lets make sure the fiwareclient is correctly set up
	fiwareclient_relative_path = ('../' + fiwareclient_path[:-1]).replace('/', '\/')
	local("sed -i 's/-e fiwareclient/-e {fiwareclient}/g' \
		{horizon}requirements.txt".format(fiwareclient=fiwareclient_relative_path,
											horizon=horizon_path))
	client = _fiwareclient_check_installation(fiwareclient_path)
	with lcd(horizon_path):
		local('sudo python tools/install_venv.py')
		local('cp openstack_dashboard/local/local_settings.py.example \
			openstack_dashboard/local/local_settings.py')
	print 'Done!'
		
def horizon_dev_runserver(address='127.0.0.1:8000', horizon_path=HORIZON_ROOT):
	"""Run horizon server for development purposes"""
	with lcd(horizon_path):
		local('sudo tools/with_venv.sh python manage.py runserver \
			{0}'.format(address))


# KEYSTONE
def keystone_deploy(dev=False):
	"""Fully installs the IdM backend"""
	# TODO(garcianavalon) PARAMETERS!!!
	keystone_install()
	keystone_database_create()
	keystone_service_create()
	keystone_service_start()
	keystone_database_init()
	if dev:
		keystone_service_stop()
		print 'Run fab keystone_dev_server on another terminal to \
			run keystone\'s dev server'

# Install and configure Keystone
# Change directory to default after tests
def keystone_install(keystone_path=KEYSTONE_ROOT):
	print 'Installing backend (Keystone)'
	local('git clone https://github.com/ging/keystone.git \
		{0}'.format(keystone_path))
	with lcd(keystone_path):
		local('sudo apt-get install python-dev libxml2-dev \
			libxslt1-dev libsasl2-dev libsqlite3-dev libssl-dev \
			libldap2-dev libffi-dev')
		local('python tools/install_venv.py')
		local('cp etc/keystone.conf.sample etc/keystone.conf')
		# Uncomment config file
		with lcd('etc/'):
			local("sed -i 's/#admin_token/admin_token/g' keystone.conf")
			local("sed -i 's/#admin_port/admin_port/g' keystone.conf")
			local("sed -i 's/#public_port/public_port/g' keystone.conf")
	print 'Done!'

# Create database
def keystone_database_create(keystone_path=KEYSTONE_ROOT):
	with lcd(keystone_path):
		local('sudo tools/with_venv.sh bin/keystone-manage db_sync')
		local('sudo tools/with_venv.sh bin/keystone-manage db_sync \
			--extension=oauth2')
		local('sudo tools/with_venv.sh bin/keystone-manage db_sync \
			--extension=roles')
		local('sudo tools/with_venv.sh bin/keystone-manage db_sync \
			--extension=user_registration')


# Start keystone service
def keystone_service_start():
	local('sudo service keystone_idm start')
	
# Stop keystone service
def keystone_service_stop():
	local('sudo service keystone_idm stop')
	
# Configure keystone as a service
# @param username: directory home/{username}/...
def keystone_service_create(absolute_keystone_path=None):
	if not absolute_keystone_path:
		absolute_keystone_path = os.getcwd() + '/' + KEYSTONE_ROOT
	from string import Template
	in_file = open('keystone_idm.conf')
	src = Template(in_file.read())
	out_file = open("tmp_keystone_idm.conf", "w")
	out_file.write(src.substitute({
		'absolute_keystone_path': absolute_keystone_path}))
	out_file.close()
	local('sudo cp tmp_keystone_idm.conf /etc/init/keystone_idm.conf')
	local('sudo rm tmp_keystone_idm.conf')

# Keystone stop service and remove database
def keystone_database_delete(keystone_path=KEYSTONE_ROOT):
	db_path = keystone_path + 'keystone.db'
	if os.path.isfile(db_path):
		local('sudo rm ' + db_path)

def keystone_database_init(keystone_path=KEYSTONE_ROOT, 
						fiwareclient_path=FIWARECLIENT_ROOT,
						internal_address=CONTROLLER_INTERNAL_ADDRESS, 
						public_address=CONTROLLER_PUBLIC_ADDRESS,
						admin_address=CONTROLLER_ADMIN_ADDRESS):

	client = _fiwareclient_check_installation(fiwareclient_path)
	Endpoint = namedtuple('Enpoint', 'url interface')
	def create_service_and_enpoints(name, endpoint_type, description, endpoints):
		service = keystone.services.create(name=name, type=endpoint_type, 
											description=description)
		for endpoint in endpoints:
			keystone.endpoints.create(region='RegionOne', 
									service=service,
									url=endpoint.url,
									interface=endpoint.interface)

	config = ConfigParser.ConfigParser()
	config.read(keystone_path + 'etc/keystone.conf')
	try:
		admin_port = config.defaults()['admin_port']
		public_port = config.defaults()['public_port']
		token = os.getenv('OS_SERVICE_TOKEN', config.defaults()['admin_token'])
		print admin_port, public_port, token

		# Passwords are either environment variables or their default value
		ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'secrete')
		IDM_PASSWORD = os.getenv('IDM_PASSWORD', 'idm')
		GLANCE_PASSWORD = os.getenv('SERVICE_PASSWORD', 'glance')
		NOVA_PASSWORD = os.getenv('SERVICE_PASSWORD', 'nova')
		EC2_PASSWORD = os.getenv('SERVICE_PASSWORD', 'ec2')
		SWIFT_PASSWORD = os.getenv('SERVICE_PASSWORD', 'swiftpass')

		# Controller Addresses		
		print public_address, admin_address, internal_address

		endpoint = 'http://{ip}:{port}/v3'.format(ip='127.0.0.1', port=admin_port)
		keystone = client.Client(token=token, endpoint=endpoint)
		print 'Connected to keystone using token'

		# Default keystone roles
		# NOTE(garcianavalon) don't confuse it with keystone v2 API
		# default role (member_role_name=_member_). We need a default
		# role to add users to projects. Horizon knows this role throught
		# the local_settings.py file.
		member_role = keystone.roles.create(name='member')
		admin_role = keystone.roles.create(name='admin')
		print 'created default keystone roles'
		#Default Tenant
		
		demo_tenant = keystone.projects.create(name='demo', 
											description='Default Tenant',
											domain='default')
		admin_user = keystone.users.create(name='admin', 
										password=ADMIN_PASSWORD, 
										default_project=demo_tenant,
										domain='default')
		keystone.roles.grant(user=admin_user, 
							role=admin_role, 
							project=demo_tenant)
		
		#idm Tenant
		idm_tenant = keystone.projects.create(name='idm', 
									description='Tenant for the idm user', 
									is_defaut=True, 
									domain='default')
		idm_user = keystone.users.create(name='idm', 
									password=IDM_PASSWORD,
									default_project=idm_tenant, 
									domain='default')
		keystone.roles.grant(user=idm_user, 
							role=admin_role, 
							project=idm_tenant)

		#Service Tenant
		service_tenant = keystone.projects.create(name='service', 
											description='Service Tenant', 
											is_defaut=True, 
											domain='default')

		glance_user = keystone.users.create(name='glance', 
											password=GLANCE_PASSWORD, 
											domain='default')
		keystone.roles.grant(user=glance_user, 
							role=admin_role, 
							project=service_tenant)
		nova_user = keystone.users.create(name='nova', 
										password=NOVA_PASSWORD,
										default_project=service_tenant,  
										domain='default')
		keystone.roles.grant(user=nova_user, 
							role=admin_role, 
							project=service_tenant)
		ec2_user = keystone.users.create(name='ec2', 
										password=EC2_PASSWORD,
										default_project=service_tenant,  
										domain='default')
		keystone.roles.grant(user=ec2_user, 
							role=admin_role, 
							project=service_tenant)
		swift_user = keystone.users.create(name='swift', 
										password=SWIFT_PASSWORD,
										default_project=service_tenant,  
										domain='default')
		keystone.roles.grant(user=swift_user, 
							role=admin_role, 
							project=service_tenant)
		print 'Created default projects and users.'

		# Keystone service
		keystone_endpoints = [
			Endpoint('http://{public_address}:5000/v3'
				.format(public_address=public_address), 'public'),
			Endpoint('http://{admin_address}:5000/v3'
				.format(admin_address=admin_address), 'admin'),
			Endpoint('http://{internal_address}:5000/v3'
				.format(internal_address=internal_address), 'internal')
		]
		create_service_and_enpoints('keystone', 'identity', 
									'Keystone Identity Service', keystone_endpoints)

		# Nova service
		nova_endpoints = [
			Endpoint('http://{public_address}:8774/v2/$(tenant_id)s'
				.format(public_address=public_address), 'public'),
			Endpoint('http://{admin_address}:8774/v2/$(tenant_id)s'
				.format(admin_address=admin_address), 'admin'),
		]
		create_service_and_enpoints('nova', 'compute', 
									'Nova Compute Service', nova_endpoints)
		
		# Volume service
		volume_endpoints = [
			Endpoint('http://{public_address}:8776/v1/$(tenant_id)s'
				.format(public_address=public_address), 'public'),
			Endpoint('http://{admin_address}:8776/v1/$(tenant_id)s'
				.format(admin_address=admin_address), 'admin'),
		]
		create_service_and_enpoints('volume', 'volume', 
									'Nova Volume Service', volume_endpoints)

		# Image service
		image_endpoints = [
			Endpoint('http://{public_address}:9292'
				.format(public_address=public_address), 'public'),
			Endpoint('http://{admin_address}:9292'
				.format(admin_address=admin_address), 'admin'),
		]
		create_service_and_enpoints('glance', 'image', 
									'Glance Image Service', image_endpoints)

		# EC2 service
		ec2_endpoints = [
			Endpoint('http://{public_address}:8773/services/Cloud'
				.format(public_address=public_address), 'public'),
			Endpoint('http://{admin_address}:8773/services/Cloud'
				.format(admin_address=admin_address), 'admin'),
		]
		create_service_and_enpoints('ec2', 'ec2', 
									'EC2 Compatibility Layer', ec2_endpoints)

		# Swift service
		swift_endpoints = [
			Endpoint('http://{public_address}:8080/v1/AUTH_$(tenant_id)s'
				.format(public_address=public_address), 'public'),
			Endpoint('http://{admin_address}:8080/v1/AUTH_$(tenant_id)s'
				.format(admin_address=admin_address), 'admin'),
		]
		create_service_and_enpoints('swift', 'object-store', 
									'Swift Service', swift_endpoints)
		print ('Created default services and endpoints.')

		# Default Permissions and Roles
		created_permissions = []
		for permission in INTERNAL_PERMISSIONS:
			created_permissions.append(
				keystone.fiware_roles.permissions.create(name=permission, 
													is_internal=True))
		for role in INTERNAL_ROLES:
			created_role = keystone.fiware_roles.roles.create(name=role, 
														is_internal=True)
			# Link roles with permissions
			for index in INTERNAL_ROLES[role]:
				keystone.fiware_roles.permissions.add_to_role(created_role,
												created_permissions[index])
		print ('Created default fiware roles and permissions.')
		

										
		# Create ec2 credentials 
		# result = keystone.ec2.create(project_id=service_tenant.id, user_id=admin_user.id)
		# admin_access = result.access
		# admin_secret = result.secret
	except Exception as e:
		print('Exception: {0}'.format(e))

def keystone_dev_server(keystone_path=KEYSTONE_ROOT):
	"""Runs the server in dev mode."""
	with lcd(keystone_path):
		local('sudo tools/with_venv.sh bin/keystone-all -v')

def keystone_reset(keystone_path=KEYSTONE_ROOT):
	local('fab keystone_service_stop')
	local('fab keystone_database_delete:keystone_path=\'{0}\''.format(keystone_path))
	local('fab keystone_database_create:keystone_path=\'{0}\''.format(keystone_path))
	local('fab keystone_keystone_service_start')
	local('fab keystone_database_init:keystone_path=\'{0}\''.format(keystone_path))