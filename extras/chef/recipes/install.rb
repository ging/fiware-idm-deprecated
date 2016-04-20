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

package 'git' do
  action :install
end

directory INSTALL_DIR do
  owner 'root'
  group 'root'
  action :create
end

execute 'github_download' do
  cwd INSTALL_DIR
  user 'root'
  action :run
  command 'git clone https://github.com/ging/fiware-idm.git .'
end

include_recipe 'keyrock::configure'

python_runtime '2' do
  version '2.7'
  options :system, dev_package: true
end

python_virtualenv INSTALL_DIR+'idm_tools' do
  user 'root'
  path INSTALL_DIR+'/idm_tools'
end

pip_requirements INSTALL_DIR+'/requirements.txt' do
  virtualenv INSTALL_DIR+'idm_tools'
end

# Install Keystone back-end
bash 'keystone_install' do
  user 'root'
  cwd INSTALL_DIR
  code <<-EOH
    source idm_tools/bin/activate
    fab keystone.install
  EOH
end

# Install Horizon front-end
bash 'horizon_install' do
  user 'root'
  cwd INSTALL_DIR
  code <<-EOH
    source idm_tools/bin/activate
    fab horizon.install
  EOH
end

# Run IdM
include_recipe 'keyrock::start'