# fix source
bash :fix_source do
  code <<-EOH
    rm /bin/sh && ln -s /bin/bash /bin/sh
  EOH
end

# Install Ubuntu dependencies
bash :set_dependencies do
  code <<-EOH
    sudo apt-get update && \
    sudo apt-get install -y wget python python-dev git && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py
  EOH
end


# Install virtualenvwrapper
bash :install_wrapper do
  code <<-EOH
    pip install virtualenvwrapper && \
    export WORKON_HOME=~/venvs && \
    mkdir -p $WORKON_HOME
  EOH
end


# Download latest version of the code
bash :download_version do
  code <<-EOH
    git clone https://github.com/ging/fiware-idm idm && \
    cd idm && \
    cp conf/settings.py.example conf/settings.py
  EOH
end

# Install python dependecies
bash :install_pydems do
  apppath =  node[fiware-idm][:app_dir]
  code <<-EOH
    cd #{node.default[:app_dir]}
    source /usr/local/bin/virtualenvwrapper.sh && \
    mkvirtualenv idm_tools && \
    pip install -r requirements.txt
  EOH
end


# Install Keystone backend
bash :install_keystone do
  code <<-EOH
    source /usr/local/bin/virtualenvwrapper.sh && \
    workon idm_tools && \
    fab keystone.install && \
    fab keystone.database_create
  EOH
end

# Install Horizon frontend
bash :install_horizon do
  code <<-EOH
    source /usr/local/bin/virtualenvwrapper.sh && \
    workon idm_tools && \
    fab horizon.install
  EOH
end

bash :run_entrypoint do
  code <<-EOH
    cp docker-entrypoint.sh /docker-entrypoint.sh
    chmod 755 /docker-entrypoint.sh
    /docker-entrypoint.sh &&
  EOH
end