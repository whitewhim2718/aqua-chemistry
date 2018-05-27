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

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
    
with open('requirements.txt', 'r') as fh:
    requirements = fh.readlines()

setuptools.setup(
    name='qiskit_acqua_chemistry',
    version="0.1.0",  # this should match __init__.__version__
    description='QISKit ACQUA Chemistry',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.ibm.com/IBMQuantum/qiskit-acqua-chemistry',
    author='QISKit ACQUA Chemistry Development Team',
    author_email='qiskit@us.ibm.com',
    license='Apache-2.0',
    classifiers=(
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering"
    ),
    keywords=['ibm', 'qiskit', 'sdk', 'quantum', 'acqua', 'chemistry'],
    packages=setuptools.find_packages(exclude=['test*']),
    install_requires=requirements,
    include_package_data=True,
    python_requires=">=3.5"
)