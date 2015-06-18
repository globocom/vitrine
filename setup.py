#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of vitrine.
# https://github.com/globocom/vitrine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Globo.com <talentos@corp.globo.com>

from setuptools import setup, find_packages
from vitrine import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='vitrine',
    version=__version__,
    description='A vitrine to showcase projects developed by Globo.com',
    long_description='''
A vitrine to showcase projects developed by Globo.com
''',
    keywords='vitrine projects teams',
    author='Globo.com',
    author_email='talentos@corp.globo.com',
    url='https://github.com/globocom/vitrine',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'Flask>=0.10.0,<0.11.0',
        'derpconf>=0.7.0,<0.8.0',
        'flask-debugtoolbar>=0.9.0,<0.10.0',
        'flask-assets>=0.10',
        'cssmin>=0.2.0,<0.3.0',
        'Flask-Script>=2.0.0,<2.1.0',
        'flask-mongoengine>=0.7.0,<0.8.0',
        'pymongo<3.0.0',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            'vitrine=vitrine.app:main',
            'vitrine-manage=vitrine.manage:main',
        ],
    },
)
