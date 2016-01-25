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


# class CheckTask(Task):
#     """Run several checks in the Front-end settings file."""
#     name = "check"

#     def run(self, horizon_path, warnings=False, unattended=False):
#         #   returns 1 if everything went OK, 0 otherwise
#         print 'Checking Horizon... ',
#         check1 = self._check_for_new_settings(horizon_path + 'openstack_dashboard/local/', warnings)
#         check2 = self._check_for_roles_ids(horizon_path + 'openstack_dashboard/local/', unattended)
#         return check1 and check2

#     def _parse_setting(self, setting):
#         if '=' in setting:
#             if '#' in setting:
#                 if setting[1] == ' ':
#                     return setting[setting.find('#')+2:setting.find('=')]
#                 else:
#                     return setting[setting.find('#')+1:setting.find('=')]
#             else:
#                 if setting[1] == ' ':
#                     return setting[1:setting.find('=')]
#                 return setting[0:setting.find('=')]

#     def _check_for_new_settings(self, settings_path, warnings=False):
#         """Checks for new settings in the template which don't exist in the current file"""
#         # returns 1 if everything went OK, 0 otherwise
#         with open(settings_path+'local_settings.py', 'r') as old_file,\
#              open(settings_path+'local_settings.py.example', 'r') as new_file:
#             old = set(old_file)
#             new = set(new_file)

#         new_settings = set()
#         old_settings = set()

#         # remove values to have settings' names
#         for s in new.difference(old):
#             new_settings.add(self._parse_setting(s))
#         for s in old.difference(new):
#             old_settings.add(self._parse_setting(s))

#         latest_settings = new_settings.difference(old_settings)

#         created_settings = old_settings.difference(new_settings)

#         if warnings and created_settings:
#             print yellow('[Warning] the followind settings couldn\'t be found in the settings template: ')
#             for s in created_settings:
#                 print '\t'+yellow(s)

#         if not latest_settings:
#             print green('Settings OK.'),
#             return 1 # flag for the main task
#         else:
#             print red('Some errors were encountered:')
#             print red('The following settings couldn\'t be found in your local_settings.py module:')
#             settings_to_write = list()
#             for s in latest_settings:
#                 with open(settings_path+'local_settings.py.example', 'r') as template:
#                     block = 0
#                     for line in template.readlines():
#                         if s in line or block > 0:
#                             settings_to_write.append(line)
#                             if '{' in line: block += 1
#                             if '}' in line: block -= 1
#                 print '\t'+red(s)

#             autofix = prompt(red('Would you like to add defaults for the missing settings? [Y/n]: '),\
#                              default='n', validate='[Y,n]')
#             if autofix == 'Y':
#                 with open(settings_path+'local_settings.py', 'a') as output:
#                     output.write('\n\n# --- NEW SETTINGS ADDED AUTOMATICALLY ---\n')
#                     for s in settings_to_write:
#                         output.write(s)
#                 print green('The missing settings were added.\nPlease check the local_settings.py module to make any necessary changes.')

#             else:
#                 print red('Please edit the local_settings.py module manually so that it contains the settings above.')
#             return 0 # flag for the main task


# instance = CheckTask()
