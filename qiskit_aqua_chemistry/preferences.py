# -*- coding: utf-8 -*-

# Copyright 2018 IBM.
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
# =============================================================================

import os
import json
import re
import copy
import qiskit_aqua
from qiskit_aqua_chemistry import AquaChemistryError

class Preferences(object):
   
    PACKAGE_TYPE_DRIVERS = 'drivers'
    PACKAGE_TYPE_CHEMISTRY = 'chemistry'
    _FILENAME = '.qiskit_aqua_chemistry'
    _VERSION = '1.0'
    _QCONFIG_NAME = 'Qconfig'
    URL = 'https://quantumexperience.ng.bluemix.net/api'
    VERIFY = True
    
    def __init__(self):
        """Create Preferences object."""
        self._preferences = { 
                'version' : Preferences._VERSION
        }
        self._packages_changed = False
        self._qconfig_changed = False
        self._logging_config_changed = False
        self._token = None
        self._url = Preferences.URL
        self._hub = None
        self._group = None
        self._project = None
        self._verify = Preferences.VERIFY
        self._proxy_urls = None
        template_file = os.path.join(os.path.dirname(__file__), 'Qconfig_template.txt')
        self._qconfig_template = []
        with open(template_file, 'r') as stream:
            for line in stream:
                self._qconfig_template.append(line)
            
        qconfig = qiskit_aqua.get_qconfig()
        if qconfig is not None:
            self._token = qconfig.APItoken
            if 'url' in qconfig.config:
                self._url = qconfig.config['url'] 
            if 'hub' in qconfig.config:
                self._hub = qconfig.config['hub']
            if 'group' in qconfig.config:
                self._group = qconfig.config['group']
            if 'project' in qconfig.config:
                self._project = qconfig.config['project']
            if 'verify' in qconfig.config:
                self._verify = qconfig.config['verify']
            if 'proxies' in qconfig.config and isinstance(qconfig.config['proxies'],dict) and 'urls' in qconfig.config['proxies']:
                self._proxy_urls = qconfig.config['proxies']['urls']
            
        home = os.path.expanduser("~")
        self._filepath = os.path.join(home,Preferences._FILENAME)
        try:
            with open(self._filepath) as json_pref:
                self._preferences = json.load(json_pref)
        except:
            pass
            
    def save(self):
        if self._qconfig_changed:
            token = "'" + self._token + "'" if self._token is not None else 'None'
            url = "'" + self._url + "'" if self._url is not None else 'None'
            hub = "'" + self._hub + "'" if self._hub is not None else 'None'
            group = "'" + self._group + "'" if self._group is not None else 'None'
            project = "'" + self._project + "'" if self._project is not None else 'None'
            verify = str(self._verify) if self._verify is not None else 'None'
            proxies = { 'urls': self._proxy_urls } if self._proxy_urls is not None else {}
            proxies = json.dumps(proxies, sort_keys=True, indent=4) if proxies is not None else 'None'
            qconfig_content = [re.sub('&APItoken', token, l) for l in self._qconfig_template]
            qconfig_content = [re.sub('&url', url, l) for l in qconfig_content]
            qconfig_content = [re.sub('&hub', hub, l) for l in qconfig_content]
            qconfig_content = [re.sub('&group', group, l) for l in qconfig_content]
            qconfig_content = [re.sub('&project', project, l) for l in qconfig_content]
            qconfig_content = [re.sub('&verify', verify, l) for l in qconfig_content]
            qconfig_content = [re.sub('&proxies', proxies, l) for l in qconfig_content]
            path = self.get_qconfig_path(os.path.abspath(os.path.join(os.getcwd(),Preferences._QCONFIG_NAME + '.py')))
            with open(path, 'w') as stream:
                stream.write(''.join(qconfig_content))
                
            self._qconfig_changed = False
            qconfig = qiskit_aqua.discover_qconfig(os.getcwd())
            if qconfig is not None:
                qiskit_aqua.set_qconfig(qconfig)
        
        if self._logging_config_changed or self._packages_changed:
            with open(self._filepath, 'w') as fp:
                json.dump(self._preferences, fp, sort_keys=True, indent=4) 
            self._logging_config_changed = False
            self._packages_changed = False
        
    def get_version(self):
        if 'version' in self._preferences:
            return self._preferences['version']
        
        return None
        
    def get_qconfig_path(self,default_value=None):
        qconfig = qiskit_aqua.get_qconfig()
        if qconfig is not None:
            return os.path.abspath(qconfig.__file__)
       
        return default_value
        
    def get_token(self,default_value=None):
        if self._token is not None:
            return self._token
        
        return default_value
    
    def set_token(self,token):
        if self._token != token:
            self._qconfig_changed = True
            self._token = token
        
    def get_url(self,default_value=None):
        if self._url is not None:
            return self._url
        
        return default_value
    
    def set_url(self,url):
        if self._url != url:
            self._qconfig_changed = True
            self._url = url
        
    def get_hub(self,default_value=None):
        if self._hub is not None:
            return self._hub
        
        return default_value
    
    def set_hub(self,hub):
        if self._hub != hub:
            self._qconfig_changed = True
            self._hub = hub
        
    def get_group(self,default_value=None):
        if self._group is not None:
            return self._group
        
        return default_value
    
    def set_group(self,group):
        if self._group != group:
            self._qconfig_changed = True
            self._group = group
        
    def get_project(self,default_value=None):
        if self._project is not None:
            return self._project
        
        return default_value
    
    def set_project(self,project):
       if self._project != project:
            self._qconfig_changed = True
            self._project = project
            
    def get_verify(self, default_value=None):
        if self._verify is not None:
            return self._verify

        return default_value

    def set_verify(self, verify):
        if self._verify != verify:
            self._qconfig_changed = True
            self._verify = verify
            
    def get_proxy_urls(self, default_value=None):
        if self._proxy_urls is not None:
            return copy.deepcopy(self._proxy_urls)

        return default_value

    def set_proxy_urls(self, proxy_urls):
        if self._proxy_urls != proxy_urls:
            self._qconfig_changed = True
            self._proxy_urls = proxy_urls
            
    def get_packages(self, package_type, default_value=None):
        if package_type is not None and isinstance(package_type,str) and \
            'packages' in self._preferences and self._preferences['packages'] is not None and \
            package_type in self._preferences['packages'] and self._preferences['packages'][package_type] is not None:
            return copy.deepcopy(self._preferences['packages'][package_type])

        return default_value
    
    def add_package(self, package_type, package):
        if package_type is not None and isinstance(package_type,str) and package is not None and isinstance(package,str): 
            if package_type != Preferences.PACKAGE_TYPE_DRIVERS and package_type != Preferences.PACKAGE_TYPE_CHEMISTRY:
                raise AquaChemistryError('Invalid package type {}'.format(package_type))
                
            packages = self.get_packages(package_type,[])
            if package not in packages:
                packages.append(package)
                if 'packages' in self._preferences and self._preferences['packages'] is not None:
                    self._preferences['packages'][package_type] = packages
                else:
                    self._preferences['packages'] = { package_type : packages }
                    
                self._packages_changed = True
                return True
            
        return False
    
    def change_package(self, package_type, old_package, new_package):
        if package_type is not None and isinstance(package_type,str) and \
            old_package is not None and isinstance(old_package,str) and \
            new_package is not None and isinstance(new_package,str): 
            if package_type != Preferences.PACKAGE_TYPE_DRIVERS and package_type != Preferences.PACKAGE_TYPE_CHEMISTRY:
                raise AquaChemistryError('Invalid package type {}'.format(package_type))
                
            packages = self.get_packages(package_type,[])
            for index,package in enumerate(packages):
                if package == old_package:
                    packages[index] = new_package
                    if 'packages' in self._preferences and self._preferences['packages'] is not None:
                        self._preferences['packages'][package_type] = packages
                    else:
                        self._preferences['packages'] = { package_type : packages }
                    
                    self._packages_changed = True
                    return True
            
        return False
                
    def remove_package(self, package_type, package):
        if package_type is not None and isinstance(package_type,str) and package is not None and isinstance(package,str): 
            packages = self.get_packages(package_type,[])
            if package in packages:
                packages.remove(package)
                if 'packages' in self._preferences and self._preferences['packages'] is not None:
                    self._preferences['packages'][package_type] = packages
                else:
                    self._preferences['packages'] = { package_type : packages }
                        
                self._packages_changed = True
                return True
            
        return False
    
    def set_packages(self, package_type, packages):
        if package_type is not None and isinstance(package_type,str): 
            if package_type != Preferences.PACKAGE_TYPE_DRIVERS and package_type != Preferences.PACKAGE_TYPE_CHEMISTRY:
                raise AquaChemistryError('Invalid package type {}'.format(package_type))
                
            if 'packages' in self._preferences and self._preferences['packages'] is not None:
                self._preferences['packages'][package_type] = packages
            else:
                self._preferences['packages'] = { package_type : packages }
                    
            self._packages_changed = True
            return True
            
        return False
    
        self._packages_changed = True
        self._preferences['packages'] = packages
    
    def get_logging_config(self,default_value=None):
        if 'logging_config' in self._preferences:
            return self._preferences['logging_config']
        
        return default_value
    
    def set_logging_config(self,logging_config):
        self._logging_config_changed = True
        self._preferences['logging_config'] = logging_config
