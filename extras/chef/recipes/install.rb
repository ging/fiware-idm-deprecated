#
# Cookbook Name:: keyrock
# Recipe:: install
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

include_recipe 'keyrock::stop'
include_recipe 'keyrock::uninstall'

# Checking OS compatibility for idm
if node['platform'] != 'ubuntu'
  log '*** Sorry, but the fiware idm requires a ubuntu OS ***'
end
return if node['platform'] != 'ubuntu'

pkg_depends = value_for_platform_family(
    'default' => %w(wget python git vim expect python-dev python-virtualenv libssl-dev libffi-dev libjpeg8-dev libxml2-dev libxslt1-dev libsasl2-dev libssl-dev libldap2-dev libffi-dev libsqlite3-dev libmysqlclient-dev python-mysqldb)
)

pkg_depends.each do |pkg|
  package pkg do
    action :install
  end
end

directory INSTALL_DIR do
  owner 'root'
  group 'root'
  action :create
end

bash 'no_terminal' do
  user 'root'
  command 'export DEBIAN_FRONTEND=noninteractive'
end

# Download latest version of the code
bash 'github_download' do
  cwd INSTALL_DIR
  user 'root'
  code <<-EOH
git clone https://github.com/ging/keystone
(cd keystone && git checkout tags/keyrock-6.0.0)
git clone https://github.com/ging/horizon
(cd horizon && git checkout tags/keyrock-6.0.0)
  EOH
end

bash 'python_venv' do
  cwd INSTALL_DIR
  user 'root'
  code <<-EOH
python keystone/tools/install_venv.py
python horizon/tools/install_venv.py
  EOH
end

# Sync database
bash 'sync_db' do
  cwd INSTALL_DIR
  user 'root'
  code <<-EOH
(cd keystone && sudo tools/with_venv.sh bin/keystone-manage db_sync && \
sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=endpoint_filter && \
sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=oauth2 && \
sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=roles && \
sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=user_registration && \
sudo tools/with_venv.sh bin/keystone-manage db_sync --extension=two_factor_auth )
  EOH
end



include_recipe 'keyrock::configure'

# Run IdM
include_recipe 'keyrock::start'