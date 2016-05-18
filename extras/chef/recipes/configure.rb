#
# Cookbook Name:: keyrock
# Recipe:: configure
#
# Copyright 2015, GING, ETSIT, UPM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
INSTALL_DIR = "#{node['keyrock'][:install_dir]}"

## Creating keyrock config files
remote_file 'Copy horizon config file' do
  path "#{INSTALL_DIR}/horizon/openstack_dashboard/local/local_settings.py"
  source "file://#{INSTALL_DIR}/horizon/openstack_dashboard/local/local_settings.py.example"
  owner 'root'
  group 'root'
  mode 0755
  not_if { ::File.exists?("#{INSTALL_DIR}/horizon/openstack_dashboard/local/local_settings.py") }
end

# Set up idm password
bash 'populate DB' do
  cwd INSTALL_DIR
  user 'root'
  code <<-EOH
wget https://raw.githubusercontent.com/ging/fiware-idm/master/extras/scripts/expect_idm_password
chmod +x expect_idm_password
cd keystone
sudo ../expect_idm_password
EOH
end

ruby_block 'Setup IDM password' do
  block do
    fe = Chef::Util::FileEdit.new("#{INSTALL_DIR}/horizon/openstack_dashboard/local/local_settings.py")
    fe.search_file_replace(/\$\$IDM_PASS/, 'idm')
    fe.write_file
  end
end

remote_file 'Copy keystone config file' do
  path "#{INSTALL_DIR}/keystone/etc/keystone.conf"
  source "file://#{INSTALL_DIR}/keystone/etc/keystone.conf.sample"
  owner 'root'
  group 'root'
  mode 0755
  not_if { ::File.exists?("#{INSTALL_DIR}/keystone/etc/keystone.conf") }
end

file '/etc/init/horizon_idm.conf' do
  owner 'root'
  group 'root'
  mode 0755
  content <<-EOH
 # horizon_idm - horizon_idm job file
description "Service conf file for the IdM frontend based in Horizon"
start on (local-filesystems and net-device-up IFACE!=lo)
stop on runlevel [016]
# Automatically restart process if crashed
respawn
setuid root
script
cd #{INSTALL_DIR+'/horizon'}
#activate the venv
. .venv/bin/activate
#run horizon
python manage.py runserver 0.0.0.0:8000
end script
  EOH
end

file '/etc/init/keystone_idm.conf' do
  owner 'root'
  group 'root'
  mode 0755
  content <<-EOH
# keystone_idm - keystone_idm job file
description "Service conf file for the IdM backend based in Keystone"
author "Enrique Garcia Navalon <garcianavalon@gmail.com>"
start on (local-filesystems and net-device-up IFACE!=lo)
stop on runlevel [016]
# Automatically restart process if crashed
respawn
setuid root
script
cd #{INSTALL_DIR+'/keystone'}
#activate the venv
. .venv/bin/activate
#run keystone
bin/keystone-all
end script
  EOH
end