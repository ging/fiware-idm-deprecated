#!/bin/bash

# After a few seconds, you should get a 200 OK response and the welcoming index.html file
# This means both Keystone back-end and Horizon front-end are correctly installed and working

wget http://$IP:8000 -O /dev/null
