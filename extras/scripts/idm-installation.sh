#!/bin/bash

# Install Ubuntu dependencies
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
sudo apt-get install -y wget python git vim expect
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

# Install Ubuntu project dependencies
sudo apt-get install -y python-dev python-virtualenv libssl-dev libjpeg8-dev libxml2-dev libxslt1-dev libsasl2-dev libssl-dev libldap2-dev libffi-dev libsqlite3-dev libmysqlclient-dev python-mysqldb

# Download latest version of the code 
git clone https://github.com/ging/keystone
(cd keystone && git checkout tags/keyrock-6.0.0)

git clone https://github.com/ging/horizon
(cd horizon && git checkout tags/keyrock-6.0.0)	

# Configuring settings files
cp keystone/etc/keystone.conf.sample keystone/etc/keystone.conf
 cp horizon/openstack_dashboard/local/local_settings.py.example horizon/openstack_dashboard/local/local_settings.py
sed -i s/\$\$IDM_PASS/idm/g horizon/openstack_dashboard/local/local_settings.py

# Install python dependecies
sudo python keystone/tools/install_venv.py
sudo python horizon/tools/install_venv.py

# Sync database
(cd keystone && sudo tools/with_venv.sh bin/keystone-manage db_sync && \
sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=endpoint_filter && \
sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=oauth2 && \
sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=roles && \
sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=user_registration && \
sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=two_factor_auth )

# Set up idm password
wget https://raw.githubusercontent.com/ging/fiware-idm/master/extras/scripts/expect_idm_password
chmod +x expect_idm_password
(cd keystone && sudo ../expect_idm_password)

# Set up environment variables
ABSOLUTE_KEYROCK_PATH="$(pwd)"
ABSOLUTE_HORIZON_PATH="$(echo $ABSOLUTE_KEYROCK_PATH/horizon)"
ABSOLUTE_KEYSTONE_PATH="$(echo $ABSOLUTE_KEYROCK_PATH/keystone)"

# Install Keystone back-end and set-up service
/bin/cat <<EOT >keystone_idm.conf
# keystone_idm - keystone_idm job file
 description "Service conf file for the IdM backend based in Keystone"
 author "Enrique Garcia Navalon <garcianavalon@gmail.com>"
 start on (local-filesystems and net-device-up IFACE!=lo)
 stop on runlevel [016]
# Automatically restart process if crashed
respawn
setuid root
script
cd $ABSOLUTE_KEYSTONE_PATH
#activate the venv
. .venv/bin/activate
#run keystone
bin/keystone-all
end script
EOT
sudo mv keystone_idm.conf /etc/init
sudo service keystone_idm start

# Install Horizon front-end and set-up service
/bin/cat <<EOM >horizon_idm.conf
# horizon_idm - horizon_idm job file
description "Service conf file for the IdM frontend based in Horizon"
start on (local-filesystems and net-device-up IFACE!=lo)
stop on runlevel [016]
# Automatically restart process if crashed
respawn
setuid root
script
cd $ABSOLUTE_HORIZON_PATH
#activate the venv
. .venv/bin/activate
#run horizon
python manage.py runserver 0.0.0.0:8000
end script
EOM
sudo mv horizon_idm.conf /etc/init
sudo service horizon_idm start