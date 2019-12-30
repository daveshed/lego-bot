# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools


setuptools.setup(
    name='daveshed-adafruit-jointcontroller',

    version='0.0.0',

    description='',
    long_description='',

    author='Dave Mohamad',
    author_email='davidkmohamad@gmail.com',

    license='Apache Software License',

    install_requires=[
        'Adafruit_PCA9685',
        'pyftdi',
        'daveshed-legobot'
    ],

    packages=setuptools.find_namespace_packages(include=['daveshed.*']),
    zip_safe=False,
)