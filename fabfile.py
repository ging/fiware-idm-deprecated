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
import os.path

from fabric.api import local
from fabric.context_managers import lcd

from keystoneclient.v3 import client

IDM_ROOT = 'idm/'
KEYSTONE_ROOT = IDM_ROOT + 'keystone/'
HORIZON_ROOT = IDM_ROOT + 'horizon/'

# from fabric.api import env, run
# env.hosts = ['isabel@hpcm']

# Keystone stop service and remove database
# def remove_database():
# 	with lcd('Keystone-idm/keystone/'):
# 		local('sudo service keystoneoauth2 stop')
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
# 		local('sudo service keystoneoauth2 start')

# # Set initial data for Keystone
# def data_keystone(admin_token='ADMIN', ip='127.0.0.1'):
# 	with lcd('Keystone-idm/keystone/'):
# 		local('OS_SERVICE_TOKEN={token} CONTROLLER_PUBLIC_ADDRESS={ip} \
# 			CONTROLLER_ADMIN_ADDRESS={ip} CONTROLLER_INTERNAL_ADDRESS={ip} \
# 			tools/with_venv.sh tools/sample_data.sh'.format(token=admin_token, 
# 															ip=ip))


		
# def stop_service():
# 	run('sudo service keystoneoauth2 stop')
# 	with cd('keystone'):
# 		run('sudo rm keystone.db')

# def start_service():
#	with cd('keystone'):
	# 	run('sudo tools/with_venv.sh bin/keystone-manage db_sync')
	# 	run('sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=oauth2')
	# 	run('sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=roles')
	# 	run('sudo service keystoneoauth2 start')
	# 	run('OS_SERVICE_TOKEN=ADMIN CONTROLLER_PUBLIC_ADDRESS="138.4.4.131" CONTROLLER_ADMIN_ADDRESS="138.4.4.131" CONTROLLER_INTERNAL_ADDRESS="138.4.4.131" tools/with_venv.sh tools/sample_data.sh')



#Install Horizon

def horizon_install():
	local('sudo apt-get install git python-dev python-virtualenv libssl-dev libffi-dev libjpeg8-dev')
	local('git clone https://github.com/ging/horizon.git {0}'.format(HORIZON_ROOT))
	with lcd(HORIZON_ROOT):
		local('git checkout development')
		local('git submodule init')
		local('git submodule update')
		local('sudo python tools/install_venv.py')
		local('cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py')


# Run horizon server
def horizon_runserver(ip='127.0.0.1:8000'):
	with lcd(HORIZON_ROOT):
		local('sudo tools/with_venv.sh python manage.py runserver {0}'.format(ip))


# Install and configure Keystone
# Change directory to default after tests
def keystone_install():
	local('git clone https://github.com/ging/keystone.git {0}'.format(KEYSTONE_ROOT))
	with lcd(KEYSTONE_ROOT):
		local('sudo apt-get install python-dev libxml2-dev libxslt1-dev libsasl2-dev libsqlite3-dev libssl-dev libldap2-dev libffi-dev')
		local('python tools/install_venv.py')
		local('cp etc/keystone.conf.sample etc/keystone.conf')
		#Uncomment config file
		with lcd('etc/'):
			local("sed -i 's/#admin_token/admin_token/g' keystone.conf")
			local("sed -i 's/#admin_port/admin_port/g' keystone.conf")

# Create database
def keystone_database_create():
	with lcd(KEYSTONE_ROOT):
		local('sudo tools/with_venv.sh bin/keystone-manage db_sync')
		local('sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=oauth2')
		local('sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=roles')


# Start keystone service
def keystone_service_start():
	local('sudo service keystoneoauth2 start')
	

# Stop keystone service
def keystone_service_stop():
	local('sudo service keystoneoauth2 stop')
	

# Load initial data (should be done once service is started) 
# Use 'fab intial_data' instead
def keystone_sample_data(admin_token='ADMIN', ip='127.0.0.1'):
	with lcd(KEYSTONE_ROOT):
		local('OS_SERVICE_TOKEN={token} CONTROLLER_PUBLIC_ADDRESS={ip} \
			CONTROLLER_ADMIN_ADDRESS={ip} CONTROLLER_INTERNAL_ADDRESS={ip} \
			tools/with_venv.sh tools/sample_data.sh'.format(token=admin_token, 
															ip=ip))

# Configure keystone as a service
# @param username: directory home/{username}/...
def keystone_service_create(user):
	with lcd('/etc/init/'):
		if not os.path.isfile('/etc/init/keystoneoauth2.conf'):
			text = '# keystoneoauth2 - keystoneoauth2 job file\ndescription "Keystone server extended to use OAuth2.0"\nauthor "Enrique G. Navalon <garcianavalon@gmail.com>"\nstart on (local-filesystems and net-device-up IFACE!=lo)\nstop on runlevel [016]\n# Automatically restart process if crashed\nrespawn\nsetuid root\nscript\ncd /home/{user}/idm/keystone/\n#activate the venv\n. .venv/bin/activate\n#run keystone\nbin/keystone-all\nend script'.format(user=user)
			fo = open('keystoneoauth2.conf', 'wb')
			fo.write(text)
			fo.close()
			local('sudo cp keystoneoauth2.conf /etc/init/')
			local('sudo rm keystoneoauth2.conf')
		else:
			print('Service already exists in /etc/init')

# Keystone stop service and remove database
def keystone_database_delete():
	with lcd(KEYSTONE_ROOT):
		if os.path.isfile('idm/keystone/keystone.db'):
			local('sudo rm keystone.db')


def keystone_database_init(ip='127.0.0.1'):
	
	config = ConfigParser.ConfigParser()
	
	config.read('idm/keystone/etc/keystone.conf')
	try:
		admin_port = os.getenv('OS_SERVICE_ENDPOINT', config.defaults()['admin_port'])
		endpoint = 'http://{ip}:{port}/v3'.format(ip=ip, port=admin_port)
		token = os.getenv('OS_SERVICE_TOKEN', config.defaults()['admin_token'])
		
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

		keystone = client.Client(token=token, endpoint=endpoint)
		
		#Default Tenant
		demo_tenant = keystone.projects.create(name='demo', description='Default Tenant', domain='default')
		admin_user = keystone.users.create(name='admin', password=ADMIN_PASSWORD, domain='default')
		admin_role = keystone.roles.create(name='admin')
		keystone.roles.grant(user=admin_user, role=admin_role, project=demo_tenant)
		
		#idm Tenant
		idm_tenant = keystone.projects.create(name='idm', description='Tenant for the idm user', is_defaut=True, domain='default')
		idm_user = keystone.users.create(name='idm', password=IDM_PASSWORD, domain='default')
		keystone.roles.grant(user=idm_user, role=admin_role, project=idm_tenant)

		#Service Tenant
		service_tenant = keystone.projects.create(name='service', description='Service Tenant', is_defaut=True, domain='default')

		glance_user = keystone.users.create(name='glance', password=GLANCE_PASSWORD, domain='default')
		keystone.roles.grant(user=glance_user, role=admin_role, project=service_tenant)
		nova_user = keystone.users.create(name='nova', password=NOVA_PASSWORD, domain='default')
		keystone.roles.grant(user=nova_user, role=admin_role, project=service_tenant)
		ec2_user = keystone.users.create(name='ec2', password=EC2_PASSWORD, domain='default')
		keystone.roles.grant(user=ec2_user, role=admin_role, project=service_tenant)
		swift_user = keystone.users.create(name='swift', password=SWIFT_PASSWORD, domain='default')
		keystone.roles.grant(user=swift_user, role=admin_role, project=service_tenant)

		# Keystone service
		keystone_service = keystone.services.create(name='keystone', type='identity', description="Keystone Identity Service")
		keystone.endpoints.create(
			region='RegionOne', 
			service=keystone_service,
			url='http://{public_address}:5000/v3'.format(public_address=public_address),
			interface='puadfasfblic')
		keystone.endpoints.create(
			region='RegionOne', 
			service=keystone_service,
			url='http://{public_address}:5000/v3'.format(public_address=public_address),
			interface='admin')
			# publicurl='http://{public_address}:{public_port}/v2.0'.format(public_address=public_address, public_port=public_port),
			# adminurl='http://{admin_address}:{admin_port}/v2.0'.format(admin_address=admin_address, admin_port=admin_port),
			# internalurl='http://{internal_address}:{public_port}/v2.0'.format(internal_address=internal_address, public_port=public_port))

		# Nova service
		nova_service = keystone.services.create(name='nova', type='compute', description='Nova Compute Service')
		keystone.endpoints.create(
			region='RegionOne', 
			service=nova_service.id,
			url='http://{public_address}:8774/v2/%(project_id)s'.format(public_address=public_address),
			interface='public')
		keystone.endpoints.create(
			region='RegionOne', 
			service=nova_service.id,
			url='http://{public_address}:8774/v2/%(project_id)s'.format(public_address=public_address),
			interface='admin')
			# publicurl='http://{public_address}:8774/v2/%(project_id)s'.format(public_address=public_address),
			# adminurl='http://{admin_address}:8774/v2/%(project_id)s'.format(admin_address=admin_address),
			# internalurl='http://{internal_address}:8774/v2/%(project_id)s'.format(internal_address=internal_address))

		# Volume service
		volume_service = keystone.services.create(name='volume', type='volume', description='Nova Volume Service')
		keystone.endpoints.create(
			region='RegionOne', 
			service=volume_service.id,
			url='http://{public_address}:8776/v1/%(project_id)s'.format(public_address=public_address),
			interface='public')
		keystone.endpoints.create(
			region='RegionOne', 
			service=volume_service.id,
			url='http://{public_address}:8776/v1/%(project_id)s'.format(public_address=public_address),
			interface='admin')
			# publicurl='http://{public_address}:8776/v1/%(project_id)s'.format(public_address=public_address),
			# adminurl='http://{admin_address}:8776/v1/%(project_id)s'.format(admin_address=admin_address),
			# internalurl='http://{internal_address}:8776/v1/%(project_id)s'.format(internal_address=internal_address))

		# Image service
		glance_service = keystone.services.create(name='glance', type='image', description='Glance Image Service')
		keystone.endpoints.create(
			region='RegionOne', 
			service=glance_service.id,
			url='http://{public_address}:9292'.format(public_address=public_address),
			interface='public')
		keystone.endpoints.create(
			region='RegionOne', 
			service=glance_service.id,
			url='http://{public_address}:9292'.format(public_address=public_address),
			interface='admin')
			# publicurl='http://{public_address}:9292'.format(public_address=public_address),
			# adminurl='http://{admin_address}:9292'.format(admin_address=admin_address),
			# internalurl='http://{internal_address}:9292'.format(internal_address=internal_address))

		# EC2 service
		ec2_service = keystone.services.create(name='ec2', type='ec2', description='EC2 Compatibility Layer')
		keystone.endpoints.create(
			region='RegionOne', 
			service=ec2_service.id,
			url='http://{public_address}:8773/services/Cloud'.format(public_address=public_address),
			interface='public')
		keystone.endpoints.create(
			region='RegionOne', 
			service=ec2_service.id,
			url='http://{public_address}:8773/services/Cloud'.format(public_address=public_address),
			interface='admin')
			# publicurl='http://{public_address}:8773/services/Cloud'.format(public_address=public_address),
			# adminurl='http://{admin_address}:8773/services/Admin'.format(admin_address=admin_address),
			# internalurl='http://{internal_address}:8773/services/Cloud'.format(internal_address=internal_address))

		# Swift service
		swift_service = keystone.services.create(name='swift', type='object-store', description='Swift Service')
		keystone.endpoints.create(
			region='RegionOne', 
			service=volume_service.id,
			url='http://{public_address}:8080/v1/AUTH_%(project_id)s'.format(public_address=public_address),
			interface='public')
		keystone.endpoints.create(
			region='RegionOne', 
			service=volume_service.id,
			url='http://{public_address}:8080/v1/AUTH_%(project_id)s'.format(public_address=public_address),
			interface='admin')
			# publicurl='http://{public_address}:8080/v1/AUTH_%(project_id)s'.format(public_address=public_address),
			# adminurl='http://{admin_address}:8080/v1'.format(admin_address=admin_address),
			# internalurl='http://{internal_address}:8080/v1/AUTH_%(project_id)s'.format(internal_address=internal_address))

		# Default Roles
		provider = keystone.fiware_roles.roles.create(name='Provider')
		purchaser = keystone.fiware_roles.roles.create(name='Purchaser')

		# Default Permissions
		manage_app = keystone.fiware_roles.permissions.create(name='Manage the application')
		manage_roles = keystone.fiware_roles.permissions.create(name='Manage roles')
		get_assign_roles = keystone.fiware_roles.permissions.create(name='Get and assign roles')
		manage_authorizations = keystone.fiware_roles.permissions.create(name='Manage Authorizations')

		# Create ec2 credentials 
		# result = keystone.ec2.create(project_id=service_tenant.id, user_id=admin_user.id)
		# admin_access = result.access
		# admin_secret = result.secret

	except Exception as e:
		print('Exception: {0}'.format(e))


def keystone_reset():
	local('fab keystone_service_stop')
	local('fab keystone_database_remove')
	local('fab keystone_database_create')
	local('fab keystone_keystone_service_start')
	local('fab keystone_database_init')