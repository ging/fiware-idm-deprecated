name              'keyrock'
maintainer        'GING-DIT-ETSIT-UPM'
maintainer_email  'ging@dit.upm.es'
description       'A cookbook for deploying the keyrock component'
version           '5.3.0'
long_description  IO.read(File.join(File.dirname(__FILE__), 'README.md'))

depends           'build-essential'
depends           'poise-python'
depends           'apt'

%w{ ubuntu }.each do |os|
  supports os
end