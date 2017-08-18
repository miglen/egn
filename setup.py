import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='egn',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='GPL-3.0',  # example license
    description='Validator, generator and parser for Bulgarian unique citizenship numbers (EGN/ЕГН).',
    long_description=README,
    url='http://github.com/miglen/egn/',
    author='Miglen Evlogiev',
    author_email='github@miglen.com',
    classifiers=[
        'License :: OSI Approved :: GPL-3.0', 
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)
