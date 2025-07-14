# -*- coding: utf-8 -*-
#  This file is part of AC3ES Tools.
#
#  AC3ES Tools is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  AC3ES Tools is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with AC3ES Tools.  If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages

import ac3es.cli

with open('README.md') as f:
    readme = f.read()

with open('COPYING') as f:
    license = f.read()

setup(
    name='ac3es-tools',
    version=ac3es.cli.VERSION,
    description='Various tools for manipulate Ace Combat 3 game files',
    long_description=readme,
    author='Gianluigi "Infrid" Cusimano',
    author_email='infrid@infrid.com',
    url='https://loadwordteam.com',
    license=license,
    package_dir={'': 'ac3es'},
    packages=find_packages(where='ac3es', exclude=('tests', 'docs')),
    install_requires=[],
)
