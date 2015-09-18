#!/bin/bash

# Start Keystone as a Service, run Horizon using dev_server
(
    source /usr/local/bin/virtualenvwrapper.sh
    workon idm_tools
    fab keystone.start
    fab horizon.dev_server
)