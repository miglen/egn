# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='egn',
    version='0.1.5',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    license='GPL-3.0',  # example license
    description=('Validator, generator and parser '
                 'for Bulgarian unique citizenship numbers (EGN/ЕГН).'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/miglen/egn/',
    author='Miglen Evlogiev',
    author_email='github@miglen.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: GNU '
         'General Public License v3 or later (GPLv3+)'),
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points='''
        [console_scripts]
        egn=egn:main
    ''',
)
