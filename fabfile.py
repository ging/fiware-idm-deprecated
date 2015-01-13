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

from collections import namedtuple
from fabric.api import local
from fabric.context_managers import lcd

# NOTE(garcianavalon) add the fiwareclient to PYTHONPATH
import sys
sys.path.insert(1,'./fiwareclient')
from keystoneclient.v3 import client

IDM_ROOT = '../idm/'
KEYSTONE_ROOT = IDM_ROOT + 'keystone/'
HORIZON_ROOT = IDM_ROOT + 'horizon/'
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

# from fabric.api import env, run
# env.hosts = ['isabel@hpcm']

# Keystone stop service and remove database
# def remove_database():
# 	with lcd('Keystone-idm/keystone/'):
# 		local('sudo service keystone_idm stop')
# 		if os.path.isfile('keystone.db'):
# 			local('sudo rm keystone.db')

# # Create database with extensions, delete exiting database, start service
# def start_database():
# 	with lcd('Keystone-idm/keystone/'):
# 		if os.path.isfile('keystone.db'):
# 			local('sudo rm keystone.db')
# 		local('sudo tools/with_venv.sh bin/keystone-manage db_sync')
# 		local('sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=oauth2')
# 		local('sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=roles')
# 		local('sudo service keystone_idm start')

# # Set initial data for Keystone
# def data_keystone(admin_token='ADMIN', ip='127.0.0.1'):
# 	with lcd('Keystone-idm/keystone/'):
# 		local('OS_SERVICE_TOKEN={token} CONTROLLER_PUBLIC_ADDRESS={ip} \
# 			CONTROLLER_ADMIN_ADDRESS={ip} CONTROLLER_INTERNAL_ADDRESS={ip} \
# 			tools/with_venv.sh tools/sample_data.sh'.format(token=admin_token, 
# 															ip=ip))


		
# def stop_service():
# 	run('sudo service keystone_idm stop')
# 	with cd('keystone'):
# 		run('sudo rm keystone.db')

# def start_service():
#	with cd('keystone'):
	# 	run('sudo tools/with_venv.sh bin/keystone-manage db_sync')
	# 	run('sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=oauth2')
	# 	run('sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=roles')
	# 	run('sudo service keystone_idm start')
	# 	run('OS_SERVICE_TOKEN=ADMIN CONTROLLER_PUBLIC_ADDRESS="138.4.4.131" CONTROLLER_ADMIN_ADDRESS="138.4.4.131" CONTROLLER_INTERNAL_ADDRESS="138.4.4.131" tools/with_venv.sh tools/sample_data.sh')

def setup_fiwareclient():
	""" Download and install locally the fiwareclient."""
	local('sudo git submodule init')
	local('sudo git submodule update')

def teardown_fiwareclient():
	"""Remove the fiwareclient code."""
	local('sudo rm -r fiwareclient')

#Install Horizon

def horizon_install(horizon_path=HORIZON_ROOT):
	local('sudo apt-get install git python-dev python-virtualenv libssl-dev libffi-dev libjpeg8-dev')
	local('git clone https://github.com/ging/horizon.git {0}'.format(horizon_path))
	with lcd(horizon_path):
		local('git checkout development')
		local('git submodule init')
		local('git submodule update')
		local('sudo python tools/install_venv.py')
		local('cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py')


# Run horizon server
def horizon_runserver(ip='127.0.0.1:8000', horizon_path=HORIZON_ROOT):
	with lcd(horizon_path):
		local('sudo tools/with_venv.sh python manage.py runserver {0}'.format(ip))


# Install and configure Keystone
# Change directory to default after tests
def keystone_install(keystone_path=KEYSTONE_ROOT):
	local('git clone https://github.com/ging/keystone.git {0}'.format(keystone_path))
	with lcd(keystone_path):
		local('sudo apt-get install python-dev libxml2-dev libxslt1-dev libsasl2-dev libsqlite3-dev libssl-dev libldap2-dev libffi-dev')
		local('python tools/install_venv.py')
		local('cp etc/keystone.conf.sample etc/keystone.conf')
		#Uncomment config file
		with lcd('etc/'):
			local("sed -i 's/#admin_token/admin_token/g' keystone.conf")
			local("sed -i 's/#admin_port/admin_port/g' keystone.conf")

# Create database
def keystone_database_create(keystone_path=KEYSTONE_ROOT):
	with lcd(keystone_path):
		local('sudo tools/with_venv.sh bin/keystone-manage db_sync')
		local('sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=oauth2')
		local('sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=roles')


# Start keystone service
def keystone_service_start():
	local('sudo service keystone_idm start')
	

# Stop keystone service
def keystone_service_stop():
	local('sudo service keystone_idm stop')
	

# Load initial data (should be done once service is started) 
# Use 'fab intial_data' instead
def keystone_sample_data(admin_token='ADMIN', ip='127.0.0.1', 
						keystone_path=KEYSTONE_ROOT):
	with lcd(keystone_path):
		local('OS_SERVICE_TOKEN={token} CONTROLLER_PUBLIC_ADDRESS={ip} \
			CONTROLLER_ADMIN_ADDRESS={ip} CONTROLLER_INTERNAL_ADDRESS={ip} \
			tools/with_venv.sh tools/sample_data.sh'.format(token=admin_token, 
															ip=ip))

# Configure keystone as a service
# @param username: directory home/{username}/...
def keystone_service_create(user=None):
	local('sudo cp keystone_idm.conf /etc/init/')

# Keystone stop service and remove database
def keystone_database_delete(keystone_path=KEYSTONE_ROOT):
	db_path = keystone_path + 'keystone.db'
	if os.path.isfile(db_path):
		local('sudo rm ' + db_path)

def keystone_database_init(ip='127.0.0.1', keystone_path=KEYSTONE_ROOT):
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
		admin_port = os.getenv('OS_SERVICE_ENDPOINT', config.defaults()['admin_port'])
		endpoint = 'http://{ip}:{port}/v3'.format(ip=ip, port=admin_port)
		token = os.getenv('OS_SERVICE_TOKEN', config.defaults()['admin_token'])
		print admin_port, endpoint, token
		# Passwords are either environment variables or their default value
		ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'secrete')
		IDM_PASSWORD = os.getenv('IDM_PASSWORD', 'idm')
		GLANCE_PASSWORD = os.getenv('SERVICE_PASSWORD', 'glance')
		NOVA_PASSWORD = os.getenv('SERVICE_PASSWORD', 'nova')
		EC2_PASSWORD = os.getenv('SERVICE_PASSWORD', 'ec2')
		SWIFT_PASSWORD = os.getenv('SERVICE_PASSWORD', 'swiftpass')

		# Controller Addresses
		public_address = os.getenv('CONTROLLER_PUBLIC_ADDRESS', '127.0.0.1')
		admin_address = os.getenv('CONTROLLER_ADMIN_ADDRESS', 'localhost')
		internal_address = os.getenv('CONTROLLER_INTERNAL_ADDRESS', 'localhost')

		public_port = 35357
		print public_address, admin_address, internal_address, public_port

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


def keystone_reset(keystone_path=KEYSTONE_ROOT):
	local('fab keystone_service_stop')
	local('fab keystone_database_delete:keystone_path=\'{0}\''.format(keystone_path))
	local('fab keystone_database_create:keystone_path=\'{0}\''.format(keystone_path))
	local('fab keystone_keystone_service_start')
	local('fab keystone_database_init:keystone_path=\'{0}\''.format(keystone_path))