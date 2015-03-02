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

import os

from fabric.api import local
from fabric.context_managers import lcd


def install(fiwareclient_path, dev):
    """ Download and install locally the fiwareclient."""
    print 'Installing the custom keystoneclient aka fiwareclient'
    if os.path.isdir(fiwareclient_path[:-1]):
        print 'already downloaded'
    else:
        local('git clone https://github.com/ging/python-keystoneclient \
        {0}'.format(fiwareclient_path))

    with lcd(fiwareclient_path):
        if dev:
            local('git checkout development')

    local('sudo pip install -e {0}'.format(fiwareclient_path[:-1]))
    print 'Done!'