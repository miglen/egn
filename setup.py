# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='egn',
    version='0.1.4',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    license='GPL-3.0',  # example license
    description=('Validator, generator and parser '
                 'for Bulgarian unique citizenship numbers (EGN/ЕГН).'),
    long_description=long_description,
    url='http://github.com/miglen/egn/',
    author='Miglen Evlogiev',
    author_email='github@miglen.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: GNU '
         'General Public License v3 or later (GPLv3+)'),
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points='''
        [console_scripts]
        egn=egn:main
    ''',
)
