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

from conf import settings

CATALOG = [
  {
    "endpoints": [
      {
        "region": "Spain2",
        "adminURL": "http://{url}:{port}/v3/".format(
          url=settings.CONTROLLER_ADMIN_ADDRESS, port=settings.KEYSTONE_ADMIN_PORT),
        "internalURL": "http://{url}:{port}/v3/".format(
          url=settings.CONTROLLER_INTERNAL_ADDRESS, port=settings.KEYSTONE_ADMIN_PORT),
        "publicURL": "http://{url}:{port}/v3/".format(
          url=settings.CONTROLLER_PUBLIC_ADDRESS, port=settings.KEYSTONE_PUBLIC_PORT)
      }
    ],
    "type": "identity",
    "name": "keystone"
  },
  {
  	"endpoints": [
      {
      	"adminURL": "http://172.32.0.144:8774/v2/$(tenant_id)s",
      	"region": "Spain2",
      	"internalURL": "http://172.32.0.144:8774/v2/$(tenant_id)s",
      	"publicURL": "http://130.206.112.3:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://193.205.211.65:8774/v2/$(tenant_id)s",
      	"region": "Trento2",
      	"internalURL": "http://193.205.211.65:8774/v2/$(tenant_id)s",
      	"publicURL": "http://193.205.211.65:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://193.205.211.131:8774/v2/$(tenant_id)s",
      	"region": "Trento",
      	"internalURL": "http://193.205.131.65:8774/v2/$(tenant_id)s",
      	"publicURL": "http://193.205.211.131:8774/v2/$(tenant_id)s"
      },
    ],
    "type": "compute",
    "name": "nova"
  },
  {
    "endpoints": [
      {
        "adminURL": "http://172.32.0.144:9292/v1",
        "region": "Spain2",
        "internalURL": "http://172.32.0.144:9292/v1",
        "publicURL": "http://130.206.112.3:9292/v1"
      },
      {
        "adminURL": "http://193.205.211.65:9292/v1",
        "region": "Trento2",
        "internalURL": "http://193.205.211.65:9292/v1",
        "publicURL": "http://193.205.211.65:9292/v1"
      },
      {
        "adminURL": "http://193.205.211.131:9292/v1",
        "region": "Trento",
        "internalURL": "http://193.205.211.131:9292/v1",
        "publicURL": "http://193.205.211.131:9292/v1"
      },
    ],
    "type": "image",
    "name": "glance"
  },
  {
    "endpoints": [
      {
        "adminURL": "http://172.32.0.144:8776/v1/$(tenant_id)s",
        "region": "Spain2",
        "internalURL": "http://172.32.0.144:8776/v1/$(tenant_id)s",
        "publicURL": "http://130.206.112.3:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://193.205.211.65:8776/v1/$(tenant_id)s",
        "region": "Trento2",
        "internalURL": "http://193.205.211.65:8776/v1/$(tenant_id)s",
        "publicURL": "http://193.205.211.65:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://193.205.211.131:8776/v1/$(tenant_id)s",
        "region": "Trento",
        "internalURL": "http://193.205.211.131:8776/v1/$(tenant_id)s",
        "publicURL": "http://193.205.211.131:8776/v1/$(tenant_id)s"
      },
    ],
    "type": "volume",
    "name": "cinder"
  },
  {
    "endpoints": [
      {
        "adminURL": "http://172.32.0.144:8776/v2/$(tenant_id)s",
        "region": "Spain2",
        "internalURL": "http://172.32.0.144:8776/v2/$(tenant_id)s",
        "publicURL": "http://130.206.112.3:8776/v2/$(tenant_id)s"
      }
    ],
    "type": "volumev2",
    "name": "cinderv2"
  },
  {
    "endpoints": [
      {
        "adminURL": "http://172.32.0.144:9696/",
        "region": "Spain2",
        "internalURL": "http://172.32.0.144:9696/",
        "publicURL": "http://130.206.112.3:9696/"
      },
      {
        "adminURL": "http://193.205.211.65:9696/",
        "region": "Trento2",
        "internalURL": "http://193.205.211.65:9696/",
        "publicURL": "http://193.205.211.65:9696/"
      },
      {
        "adminURL": "http://193.205.211.131:9696/",
        "region": "Trento",
        "internalURL": "http://193.205.211.131:9696/",
        "publicURL": "http://193.205.211.131:9696/"
      },
    ],
    "type": "network",
    "name": "quantum"
  },
  {
    "endpoints": [
      {
        "adminURL": "http://193.205.211.65:8080/v1",
        "region": "Trento2",
        "internalURL": "http://193.205.211.65:8080/v1/AUTH_$(tenant_id)s",
        "publicURL": "http://193.205.211.65:8080/v1/AUTH_$(tenant_id)s"
      },
      {
        "adminURL": "http://193.205.211.131:8080/v1",
        "region": "Trento",
        "internalURL": "http://193.205.211.131:8080/v1/AUTH_$(tenant_id)s",
        "publicURL": "http://193.205.211.131:8080/v1/AUTH_$(tenant_id)s"
      },
    ],
    "type": "object-store",
    "name": "swift"
  },
  {
    "endpoints": [
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Trento",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Spain2",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
    ],
    "type": "sdc",
    "name": "sdc"
  },
  {
    "endpoints": [
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Trento",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Spain2",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
    ],
    "type": "paas",
    "name": "paasmanager"
  }, 
  {
    "endpoints": [
      {
        "adminURL": "http://130.206.84.4:1028/monitoring/regions/",
        "region": "Spain2",
        "internalURL": "http://130.206.84.4:1028/monitoring/regions/",
        "publicURL": "http://130.206.84.4:1028/monitoring/regions/"
      }
    ],
    "type": "monitoring",
    "name": "monitoring"
  },
  {
    "endpoints": [
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Spain2",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Trento",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
    ],
    "type": "chef-server",
    "name": "chef-server"
  },
  {
    "endpoints": [
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Spain2",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Trento",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
    ],
    "type": "puppetmaster",
    "name": "puppetmaster"
  },
  {
    "endpoints": [
      {
        "adminURL": "https://puppet-master.lab.fi-ware.org:8443/puppetwrapper/",
        "region": "Spain2",
        "internalURL": "https://puppet-master.lab.fi-ware.org:8443/puppetwrapper/",
        "publicURL": "https://puppet-master.lab.fi-ware.org:8443/puppetwrapper/"
      },
    ],
    "type": "puppetwrapper",
    "name": "puppetwrapper"
  },
]