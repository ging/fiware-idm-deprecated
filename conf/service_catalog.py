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
      	"adminURL": "http://cloud.lab.fi-ware.org:8774/v2/$(tenant_id)s",
      	"region": "Spain",
      	"internalURL": "http://cloud.lab.fi-ware.org:8774/v2/$(tenant_id)s",
      	"publicURL": "http://cloud.lab.fi-ware.org:8774/v2/$(tenant_id)s"},
      {
      	"adminURL": "http://172.32.0.144:8774/v2/$(tenant_id)s",
      	"region": "Spain2",
      	"internalURL": "http://172.32.0.144:8774/v2/$(tenant_id)s",
      	"publicURL": "http://130.206.112.3:8774/v2/$(tenant_id)s"},
      {
      	"adminURL": "http://193.205.211.65:8774/v2/$(tenant_id)s",
      	"region": "Trento2",
      	"internalURL": "http://193.205.211.65:8774/v2/$(tenant_id)s",
      	"publicURL": "http://193.205.211.65:8774/v2/$(tenant_id)s"},
      {
      	"adminURL": "http://193.205.211.131:8774/v2/$(tenant_id)s",
      	"region": "Trento",
      	"internalURL": "http://193.205.131.65:8774/v2/$(tenant_id)s",
      	"publicURL": "http://193.205.211.131:8774/v2/$(tenant_id)s"},
      {
      	"adminURL": "http://controller.xifi.imaginlab.fr:8774/v2/$(tenant_id)s",
      	"region": "Lannion",
      	"internalURL": "http://controller.xifi.imaginlab.fr:8774/v2/$(tenant_id)s",
      	"publicURL": "http://controller.xifi.imaginlab.fr:8774/v2/$(tenant_id)s"},
      {
      	"adminURL": "http://api2.xifi.imaginlab.fr:8774/v2/$(tenant_id)s",
      	"region": "Lannion2",
      	"internalURL": "http://api2.xifi.imaginlab.fr:8774/v2/$(tenant_id)s",
      	"publicURL": "http://api2.xifi.imaginlab.fr:8774/v2/$(tenant_id)s"},
      {
      	"adminURL": "http://controller1.xifi.tssg.org:8774/v2/$(tenant_id)s",
      	"region": "Waterford",
      	"internalURL": "http://controller1.xifi.tssg.org:8774/v2/$(tenant_id)s",
      	"publicURL": "http://controller1.xifi.tssg.org:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://controller2.xifi.tssg.org:8774/v2/$(tenant_id)s",
      	"region": "Waterford2",
      	"internalURL": "http://controller2.xifi.tssg.org:8774/v2/$(tenant_id)s",
      	"publicURL": "http://controller2.xifi.tssg.org:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://193.175.132.36:8774/v2/$(tenant_id)s",
      	"region": "Berlin",
      	"internalURL": "http://193.175.132.36:8774/v2/$(tenant_id)s",
      	"publicURL": "http://193.175.132.36:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://193.175.132.6:8774/v2/$(tenant_id)s",
      	"region": "Berlin2",
      	"internalURL": "http://193.175.132.6:8774/v2/$(tenant_id)s",
      	"publicURL": "http://193.175.132.6:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://195.113.161.130:8774/v2/$(tenant_id)s",
      	"region": "Prague",
      	"internalURL": "http://195.113.161.130:8774/v2/$(tenant_id)s",
      	"publicURL": "http://195.113.161.130:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://nova-api.vesnicky.cesnet.cz:8774/v2/$(tenant_id)s",
      	"region": "Prague2",
      	"internalURL": "http://nova-api.vesnicky.cesnet.cz:8774/v2/$(tenant_id)s",
      	"publicURL": "http://nova-api.vesnicky.cesnet.cz:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://filab.infotec.net.mx:8774/v2/$(tenant_id)s",
      	"region": "Mexico",
      	"internalURL": "http://filab.infotec.net.mx:8774/v2/$(tenant_id)s",
      	"publicURL": "http://filab.infotec.net.mx:8774/v2/$(tenant_id)s"
      },
     {
     	"adminURL": "http://185.23.171.2:8774/v2/$(tenant_id)s",
  	   "region": "PiraeusN",
  	   "internalURL": "http://185.23.171.2:8774/v2/$(tenant_id)s",
  	   "publicURL": "http://185.23.171.2:8774/v2/$(tenant_id)s"
     },
      {
      	"adminURL": "http://83.212.238.67:8774/v2/$(tenant_id)s",
      	"region": "PiraeusU",
      	"internalURL": "http://83.212.238.67:8774/v2/$(tenant_id)s",
      	"publicURL": "http://83.212.238.67:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://160.85.2.4:8774/v2/$(tenant_id)s",
      	"region": "Zurich",
      	"internalURL": "http://160.85.2.4:8774/v2/$(tenant_id)s",
      	"publicURL": "http://160.85.2.4:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://194.47.157.5:8774/v2/$(tenant_id)s",
      	"region": "Karlskrona",
      	"internalURL": "http://194.47.157.5:8774/v2/$(tenant_id)s",
      	"publicURL": "http://194.47.157.5:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://194.47.157.6:8774/v2/$(tenant_id)s",
      	"region": "Karlskrona2",
      	"internalURL": "http://194.47.157.6:8774/v2/$(tenant_id)s",
      	"publicURL": "http://194.47.157.6:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://194.177.207.70:8774/v2/$(tenant_id)s",
      	"region": "Volos",
      	"internalURL": "http://194.177.207.70:8774/v2/$(tenant_id)s",
      	"publicURL": "http://194.177.207.70:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://148.6.80.4:8774/v2/$(tenant_id)s",
      	"region": "Budapest",
      	"internalURL": "http://148.6.80.4:8774/v2/$(tenant_id)s",
      	"publicURL": "http://148.6.80.4:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://148.6.80.5:8774/v2/$(tenant_id)s",
      	"region": "Budapest2",
      	"internalURL": "http://148.6.80.5:8774/v2/$(tenant_id)s",
      	"publicURL": "http://148.6.80.5:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://194.28.122.3:8774/v2/$(tenant_id)s",
      	"region": "Stockholm",
      	"internalURL": "http://194.28.122.3:8774/v2/$(tenant_id)s",
      	"publicURL": "http://194.28.122.3:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://82.97.22.135:8774/v2/$(tenant_id)s",
      	"region": "SophiaAntipolis",
      	"internalURL": "http://82.97.22.135:8774/v2/$(tenant_id)s",
      	"publicURL": "http://82.97.22.135:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://150.254.155.195:8774/v2/$(tenant_id)s",
      	"region": "Poznan",
      	"internalURL": "http://150.254.155.195:8774/v2/$(tenant_id)s",
      	"publicURL": "http://150.254.155.195:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://157.193.215.181:8774/v2/$(tenant_id)s",
      	"region": "Gent",
      	"internalURL": "http://157.193.215.181:8774/v2/$(tenant_id)s",
      	"publicURL": "http://157.193.215.181:8774/v2/$(tenant_id)s"
      },
      {
      	"adminURL": "http://192.168.0.2:8774/v2/$(tenant_id)s",
      	"region": "Crete",
      	"internalURL": "http://192.168.0.2:8774/v2/$(tenant_id)s",
      	"publicURL": "http://147.27.60.1:8774/v2/$(tenant_id)s"
      }
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
      {
        "adminURL": "http://glance.lab.fi-ware.org:9292/v1",
        "region": "Spain",
        "internalURL": "http://glance.lab.fi-ware.org:9292/v1",
        "publicURL": "http://glance.lab.fi-ware.org:9292/v1"
      },
      {
        "adminURL": "http://controller.xifi.imaginlab.fr:9292/v1",
        "region": "Lannion",
        "internalURL": "http://controller.xifi.imaginlab.fr:9292/v1",
        "publicURL": "http://controller.xifi.imaginlab.fr:9292/v1"
      },
      {
        "adminURL": "http://api2.xifi.imaginlab.fr:9292/v1",
        "region": "Lannion2",
        "internalURL": "http://api2.xifi.imaginlab.fr:9292/v1",
        "publicURL": "http://api2.xifi.imaginlab.fr:9292/v1"
      },
      {
        "adminURL": "http://controller1.xifi.tssg.org:9292/v1",
        "region": "Waterford",
        "internalURL": "http://controller1.xifi.tssg.org:9292/v1",
        "publicURL": "http://controller1.xifi.tssg.org:9292/v1"
      },
      {
        "adminURL": "http://controller2.xifi.tssg.org:9292/v1",
        "region": "Waterford2",
        "internalURL": "http://controller2.xifi.tssg.org:9292/v1",
        "publicURL": "http://controller2.xifi.tssg.org:9292/v1"
      },
      {
        "adminURL": "http://193.175.132.36:9292/v1",
        "region": "Berlin",
        "internalURL": "http://193.175.132.36:9292/v1",
        "publicURL": "http://193.175.132.36:9292/v1"
      },
      {
        "adminURL": "http://193.175.132.6:9292/v1",
        "region": "Berlin2",
        "internalURL": "http://193.175.132.6:9292/v1",
        "publicURL": "http://193.175.132.6:9292/v1"
      },
      {
        "adminURL": "http://195.113.161.130:9292/v1",
        "region": "Prague",
        "internalURL": "http://195.113.161.130:9292/v1",
        "publicURL": "http://195.113.161.130:9292/v1"
      },
      {
        "adminURL": "http://glance-api.vesnicky.cesnet.cz:9292/v1",
        "region": "Prague2",
        "internalURL": "http://glance-api.vesnicky.cesnet.cz:9292/v1",
        "publicURL": "http://glance-api.vesnicky.cesnet.cz:9292/v1"
      },
      {
        "adminURL": "http://filab.infotec.net.mx:9292/v1",
        "region": "Mexico",
        "internalURL": "http://filab.infotec.net.mx:9292/v1",
        "publicURL": "http://filab.infotec.net.mx:9292/v1"
      },
      {
        "adminURL": "http://185.23.171.2:9292/v1",
        "region": "PiraeusN",
        "internalURL": "http://185.23.171.2:9292/v1",
        "publicURL": "http://185.23.171.2:9292/v1"
      },
      {
        "adminURL": "http://83.212.238.67:9292/v1",
        "region": "PiraeusU",
        "internalURL": "http://83.212.238.67:9292/v1",
        "publicURL": "http://83.212.238.67:9292/v1"
      },
      {
        "adminURL": "http://160.85.2.4:9292/v1",
        "region": "Zurich",
        "internalURL": "http://160.85.2.4:9292/v1",
        "publicURL": "http://160.85.2.4:9292/v1"
      },
      {
        "adminURL": "http://194.47.157.5:9292/v1",
        "region": "Karlskrona",
        "internalURL": "http://194.47.157.5:9292/v1",
        "publicURL": "http://194.47.157.5:9292/v1"
      },
      {
        "adminURL": "http://194.47.157.6:9292/v1",
        "region": "Karlskrona2",
        "internalURL": "http://194.47.157.6:9292/v1",
        "publicURL": "http://194.47.157.6:9292/v1"
      },
      {
        "adminURL": "http://194.177.207.70:9292/v1",
        "region": "Volos",
        "internalURL": "http://194.177.207.70:9292/v1",
        "publicURL": "http://194.177.207.70:9292/v1"
      },
      {
        "adminURL": "http://148.6.80.4:9292/v1",
        "region": "Budapest",
        "internalURL": "http://148.6.80.4:9292/v1",
        "publicURL": "http://148.6.80.4:9292/v1"
      },
      {
        "adminURL": "http://148.6.80.5:9292/v1",
        "region": "Budapest2",
        "internalURL": "http://148.6.80.5:9292/v1",
        "publicURL": "http://148.6.80.5:9292/v1"
      },
      {
        "adminURL": "http://194.28.122.3:9292/v1",
        "region": "Stockholm",
        "internalURL": "http://194.28.122.3:9292/v1",
        "publicURL": "http://194.28.122.3:9292/v1"
      },
      {
        "adminURL": "http://82.97.22.135:9292/v1",
        "region": "SophiaAntipolis",
        "internalURL": "http://82.97.22.135:9292/v1",
        "publicURL": "http://82.97.22.135:9292/v1"
      },
      {
        "adminURL": "http://150.254.155.195:9292/v1",
        "region": "Poznan",
        "internalURL": "http://150.254.155.195:9292/v1",
        "publicURL": "http://150.254.155.195:9292/v1"
      },
      {
        "adminURL": "http://157.193.215.181:9292/v1",
        "region": "Gent",
        "internalURL": "http://157.193.215.181:9292/v1",
        "publicURL": "http://157.193.215.181:9292/v1"
      },
      {
        "adminURL": "http://192.168.0.2:9292/v1",
        "region": "Crete",
        "internalURL": "http://192.168.0.2:9292/v1",
        "publicURL": "http://147.27.60.1:9292/v1"
      }
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
      {
        "adminURL": "http://cloud.lab.fi-ware.org:8776/v1/$(tenant_id)s",
        "region": "Spain",
        "internalURL": "http://cloud.lab.fi-ware.org:8776/v1/$(tenant_id)s",
        "publicURL": "http://cloud.lab.fi-ware.org:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://controller.xifi.imaginlab.fr:8776/v1/$(tenant_id)s",
        "region": "Lannion",
        "internalURL": "http://controller.xifi.imaginlab.fr:8776/v1/$(tenant_id)s",
        "publicURL": "http://controller.xifi.imaginlab.fr:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://api2.xifi.imaginlab.fr:8776/v1/$(tenant_id)s",
        "region": "Lannion2",
        "internalURL": "http://api2.xifi.imaginlab.fr:8776/v1/$(tenant_id)s",
        "publicURL": "http://api2.xifi.imaginlab.fr:8776/v1/$(tenant_id)s"
      },
      { "adminURL": "http://controller1.xifi.tssg.org:8776/v1/$(tenant_id)s",
        "region": "Waterford",
        "internalURL": "http://controller1.xifi.tssg.org:8776/v1/$(tenant_id)s",
        "publicURL": "http://controller1.xifi.tssg.org:8776/v1/$(tenant_id)s"
      },
      { "adminURL": "http://controller2.xifi.tssg.org:8776/v1/$(tenant_id)s",
        "region": "Waterford2",
        "internalURL": "http://controller2.xifi.tssg.org:8776/v1/$(tenant_id)s",
        "publicURL": "http://controller2.xifi.tssg.org:8776/v1/$(tenant_id)s"
      },
      { "adminURL": "http://193.175.132.36:8776/v1/$(tenant_id)s",
        "region": "Berlin",
        "internalURL": "http://193.175.132.36:8776/v1/$(tenant_id)s",
        "publicURL": "http://193.175.132.36:8776/v1/$(tenant_id)s"
      },
      { "adminURL": "http://193.175.132.6:8776/v1/$(tenant_id)s",
        "region": "Berlin2",
        "internalURL": "http://193.175.132.6:8776/v1/$(tenant_id)s",
        "publicURL": "http://193.175.132.6:8776/v1/$(tenant_id)s"
      },
      { "adminURL": "http://openstack.vesnicky.cesnet.cz:8776/v1/$(tenant_id)s",
        "region": "Prague",
        "internalURL": "http://openstack.vesnicky.cesnet.cz:8776/v1/$(tenant_id)s",
        "publicURL": "http://openstack.vesnicky.cesnet.cz:8776/v1/$(tenant_id)s"
      },
      { "adminURL": "http://cinder-api.vesnicky.cesnet.cz:8776/v1/$(tenant_id)s",
        "region": "Prague2",
        "internalURL": "http://cinder-api.vesnicky.cesnet.cz:8776/v1/$(tenant_id)s",
        "publicURL": "http://cinder-api.vesnicky.cesnet.cz:8776/v1/$(tenant_id)s"
      },
      { "adminURL": "http://filab.infotec.net.mx:8776/v1/$(tenant_id)s",
        "region": "Mexico",
        "internalURL": "http://filab.infotec.net.mx:8776/v1/$(tenant_id)s",
        "publicURL": "http://filab.infotec.net.mx:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://185.23.171.2:8776/v1/$(tenant_id)s",
        "region": "PiraeusN",
        "internalURL": "http://185.23.171.2:8776/v1/$(tenant_id)s",
        "publicURL": "http://185.23.171.2:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://83.212.238.67:8776/v1/$(tenant_id)s",
        "region": "PiraeusU",
        "internalURL": "http://83.212.238.67:8776/v1/$(tenant_id)s",
        "publicURL": "http://83.212.238.67:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://160.85.2.4:8776/v1/$(tenant_id)s",
        "region": "Zurich",
        "internalURL": "http://160.85.2.4:8776/v1/$(tenant_id)s",
        "publicURL": "http://160.85.2.4:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://194.47.157.5:8776/v1/$(tenant_id)s",
        "region": "Karlskrona",
        "internalURL": "http://194.47.157.5:8776/v1/$(tenant_id)s",
        "publicURL": "http://194.47.157.5:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://194.47.157.6:8776/v1/$(tenant_id)s",
        "region": "Karlskrona2",
        "internalURL": "http://194.47.157.6:8776/v1/$(tenant_id)s",
        "publicURL": "http://194.47.157.6:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://194.177.207.70:8776/v1/$(tenant_id)s",
        "region": "Volos",
        "internalURL": "http://194.177.207.70:8776/v1/$(tenant_id)s",
        "publicURL": "http://194.177.207.70:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://148.6.80.4:8776/v1/$(tenant_id)s",
        "region": "Budapest",
        "internalURL": "http://148.6.80.4:8776/v1/$(tenant_id)s",
        "publicURL": "http://148.6.80.4:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://148.6.80.5:8776/v1/$(tenant_id)s",
        "region": "Budapest2",
        "internalURL": "http://148.6.80.5:8776/v1/$(tenant_id)s",
        "publicURL": "http://148.6.80.5:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://194.28.122.3:8776/v1/$(tenant_id)s",
        "region": "Stockholm",
        "internalURL": "http://194.28.122.3:8776/v1/$(tenant_id)s",
        "publicURL": "http://194.28.122.3:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://82.97.22.135:8776/v1/$(tenant_id)s",
        "region": "SophiaAntipolis",
        "internalURL": "http://82.97.22.135:8776/v1/$(tenant_id)s",
        "publicURL": "http://82.97.22.135:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://150.254.155.195:8776/v1/$(tenant_id)s",
        "region": "Poznan",
        "internalURL": "http://150.254.155.195:8776/v1/$(tenant_id)s",
        "publicURL": "http://150.254.155.195:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://157.193.215.181:8776/v1/$(tenant_id)s",
        "region": "Gent",
        "internalURL": "http://157.193.215.181:8776/v1/$(tenant_id)s",
        "publicURL": "http://157.193.215.181:8776/v1/$(tenant_id)s"
      },
      {
        "adminURL": "http://192.168.0.2:8776/v1/$(tenant_id)s",
        "region": "Crete",
        "internalURL": "http://192.168.0.2:8776/v1/$(tenant_id)s",
        "publicURL": "http://147.27.60.1:8776/v1/$(tenant_id)s"
      }
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
      {
        "adminURL": "http://controller.xifi.imaginlab.fr:9696/",
        "region": "Lannion",
        "internalURL": "http://controller.xifi.imaginlab.fr:9696/",
        "publicURL": "http://controller.xifi.imaginlab.fr:9696/"
      },
      {
        "adminURL": "http://api2.xifi.imaginlab.fr:9696/",
        "region": "Lannion2",
        "internalURL": "http://api2.xifi.imaginlab.fr:9696/",
        "publicURL": "http://api2.xifi.imaginlab.fr:9696/"
      },
      {
        "adminURL": "http://controller1.xifi.tssg.org:9696/",
        "region": "Waterford",
        "internalURL": "http://controller1.xifi.tssg.org:9696/",
        "publicURL": "http://controller1.xifi.tssg.org:9696/"
      },
      {
        "adminURL": "http://controller2.xifi.tssg.org:9696/",
        "region": "Waterford2",
        "internalURL": "http://controller2.xifi.tssg.org:9696/",
        "publicURL": "http://controller2.xifi.tssg.org:9696/"
      },
      {
        "adminURL": "http://193.175.132.36:9696/",
        "region": "Berlin",
        "internalURL": "http://193.175.132.36:9696/",
        "publicURL": "http://193.175.132.36:9696/"
      },
      {
        "adminURL": "http://193.175.132.6:9696/",
        "region": "Berlin2",
        "internalURL": "http://193.175.132.6:9696/",
        "publicURL": "http://193.175.132.6:9696/"
      },
      {
        "adminURL": "http://filab.infotec.net.mx:9696/",
        "region": "Mexico",
        "internalURL": "http://filab.infotec.net.mx:9696/",
        "publicURL": "http://filab.infotec.net.mx:9696/",
      },
      {
        "adminURL": "http://185.23.171.2:9696/",
        "region": "PiraeusN",
        "internalURL": "http://185.23.171.2:9696/",
        "publicURL": "http://185.23.171.2:9696/"
      },
      {
        "adminURL": "http://83.212.238.67:9696/",
        "region": "PiraeusU",
        "internalURL": "http://83.212.238.67:9696/",
        "publicURL": "http://83.212.238.67:9696/"
      },
      {
        "adminURL": "http://160.85.2.4:9696/",
        "region": "Zurich",
        "internalURL": "http://160.85.2.4:9696/",
        "publicURL": "http://160.85.2.4:9696/"
      },
      {
        "adminURL": "http://194.47.157.5:9696/",
        "region": "Karlskrona",
        "internalURL": "http://194.47.157.5:9696/",
        "publicURL": "http://194.47.157.5:9696/"
      },
      {
        "adminURL": "http://194.47.157.6:9696/",
        "region": "Karlskrona2",
        "internalURL": "http://194.47.157.6:9696/",
        "publicURL": "http://194.47.157.6:9696/"
      },
      {
        "adminURL": "http://194.177.207.70:9696/",
        "region": "Volos",
        "internalURL": "http://194.177.207.70:9696/",
        "publicURL": "http://194.177.207.70:9696/"
      },
      {
        "adminURL": "http://148.6.80.4:9696/",
        "region": "Budapest",
        "internalURL": "http://148.6.80.4:9696/",
        "publicURL": "http://148.6.80.4:9696/"
      },
      {
        "adminURL": "http://148.6.80.5:9696/",
        "region": "Budapest2",
        "internalURL": "http://148.6.80.5:9696/",
        "publicURL": "http://148.6.80.5:9696/"
      },
      {
        "adminURL": "http://194.28.122.3:9696/",
        "region": "Stockholm",
        "internalURL": "http://194.28.122.3:9696/",
        "publicURL": "http://194.28.122.3:9696/"
      },
      {
        "adminURL": "http://82.97.22.135:9696/",
        "region": "SophiaAntipolis",
        "internalURL": "http://82.97.22.135:9696/",
        "publicURL": "http://82.97.22.135:9696/"
      },
      {
        "adminURL": "http://150.254.155.195:9696/",
        "region": "Poznan",
        "internalURL": "http://150.254.155.195:9696/",
        "publicURL": "http://150.254.155.195:9696/"
      },
      {
        "adminURL": "http://157.193.215.181:9696/",
        "region": "Gent",
        "internalURL": "http://157.193.215.181:9696/",
        "publicURL": "http://157.193.215.181:9696/"
      },
      {
        "adminURL": "http://192.168.0.2:9696/",
        "region": "Crete",
        "internalURL": "http://192.168.0.2:9696/",
        "publicURL": "http://147.27.60.1:9696/"
      }
    ],
    "type": "network",
    "name": "quantum"
  },
  {
    "endpoints": [
      {
        "adminURL": "http://130.206.82.9:8080/v1",
        "region": "Spain",
        "internalURL": "http://130.206.82.9:8080/v1/AUTH_$(tenant_id)s",
        "publicURL": "http://130.206.82.9:8080/v1/AUTH_$(tenant_id)s"
      },
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
      {
        "adminURL": "http://controller.xifi.imaginlab.fr:8080/v1",
        "region": "Lannion",
        "internalURL": "http://controller.xifi.imaginlab.fr:8080/v1/AUTH_$(tenant_id)s",
        "publicURL": "http://controller.xifi.imaginlab.fr:8080/v1/AUTH_$(tenant_id)s"
      },
      {
        "adminURL": "http://api2.xifi.imaginlab.fr:8080/v1",
        "region": "Lannion2",
        "internalURL": "http://api2.xifi.imaginlab.fr:8080/v1/AUTH_$(tenant_id)s",
        "publicURL": "http://api2.xifi.imaginlab.fr:8080/v1/AUTH_$(tenant_id)s"
      },
      {
        "adminURL": "http://193.1.202.143:8080/v1",
        "region": "Waterford",
        "internalURL": "http://193.1.202.143:8080/v1/AUTH_$(tenant_id)s",
        "publicURL": "http://193.1.202.143:8080/v1/AUTH_$(tenant_id)s"
      },
      {
        "adminURL": "http://193.175.132.8:8090/v1",
        "region": "Berlin",
        "internalURL": "http://193.175.132.8:8090/v1/AUTH_$(tenant_id)s",
        "publicURL": "http://193.175.132.8:8090/v1/AUTH_$(tenant_id)s"
      },
      {
        "adminURL": "http://148.6.80.5:8080/v1",
        "region": "Budapest2",
        "internalURL": "http://148.6.80.5:8080/v1/AUTH_$(tenant_id)s",
        "publicURL": "http://148.6.80.5:8080/v1/AUTH_$(tenant_id)s"
      }
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
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Spain",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Lannion",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Waterford",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Berlin",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Prague",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Mexico",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "PiraeusN",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "PiraeusU",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Karlskrona",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "SophiaAntipolis",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Volos",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Budapest",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Poznan",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Gent",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Stockholm",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Zurich",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      },
      {
        "adminURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "region": "Crete",
        "internalURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest",
        "publicURL": "https://saggita.lab.fi-ware.org:8443/sdc/rest"
      }
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
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Spain",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Lannion",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Waterford",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Berlin",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Prague",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Mexico",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "PiraeusN",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "PiraeusU",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Karlskrona",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "SophiaAntipolis",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Volos",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Budapest",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Poznan",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Gent",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Stockholm",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Zurich",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      },
      {
        "adminURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "region": "Crete",
        "internalURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest",
        "publicURL": "https://pegasus.lab.fi-ware.org:8443/paasmanager/rest"
      }
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
        "region": "Spain",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },  
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
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Berlin",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
       },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Waterford",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
       },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Prague",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Lannion",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Mexico",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "PiraeusN",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "PiraeusU",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Karlskrona",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "SophiaAntipolis",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Volos",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Budapest",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Poznan",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Gent",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Stockholm",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Zurich",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      },
      {
        "adminURL": "https://chef-server.lab.fi-ware.org",
        "region": "Crete",
        "internalURL": "https://chef-server.lab.fi-ware.org",
        "publicURL": "https://chef-server.lab.fi-ware.org"
      }
    ],
    "type": "chef-server",
    "name": "chef-server"
  },
  {
    "endpoints": [
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Spain",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
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
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Berlin",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
       },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Waterford",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
       },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Prague",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Lannion",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Mexico",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "PiraeusN",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "PiraeusU",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Karlskrona",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "SophiaAntipolis",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Volos",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Budapest",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Poznan",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Gent",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Stockholm",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Zurich",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      },
      {
        "adminURL": "http://puppet-master.lab.fi-ware.org",
        "region": "Crete",
        "internalURL": "http://puppet-master.lab.fi-ware.org",
        "publicURL": "http://puppet-master.lab.fi-ware.org"
      }
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
      {
        "adminURL": "https://puppet-master.lab.fi-ware.org:8443/puppetwrapper/",
        "region": "Spain",
        "internalURL": "https://puppet-master.lab.fi-ware.org:8443/puppetwrapper/",
        "publicURL": "https://puppet-master.lab.fi-ware.org:8443/puppetwrapper/"
      }
    ],
    "type": "puppetwrapper",
    "name": "puppetwrapper"
  },
  {
    "endpoints": [
      {
        "adminURL": "http://195.113.161.130:8774/v3",
        "region": "Prague",
        "internalURL": "http://195.113.161.130:8774/v3",
        "publicURL": "http://195.113.161.130:8774/v3"
      }
    ],
    "type": "computev3",
    "name": "novav3"
  },
  {
    "endpoints": [
      {
        "adminURL": "http://192.168.0.2:8777",
        "region": "Zurich",
        "internalURL": "192.168.0.2:8777",
        "publicURL": "http://160.85.2.4:8777"
      }
    ],
    "type": "metering",
    "name": "ceilometer"
  }
]