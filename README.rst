egn
===

Python package for validating, parsing and generating unique citizenship
numbers in Bulgaria EGN (ЕГН).

Български: Скрипт за проверка и генериране на ЕГН / Програма за проверка и генериране на единни граждански номера.

.. image:: https://badge.fury.io/py/egn.svg
   :target: https://pypi.python.org/pypi/egn
   :alt: PyPI package
.. image:: https://img.shields.io/travis/miglen/egn.svg
  :target: https://travis-ci.org/miglen/egn
.. image:: https://readthedocs.org/projects/egn/badge/?version=latest
  :target: http://egn.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status
.. image:: https://img.shields.io/codecov/c/github/miglen/egn.svg
  :target: http://codecov.io/gh/miglen/egn
.. image:: https://img.shields.io/codeclimate/github/miglen/egn.svg
  :target: https://codeclimate.com/github/miglen/egn

Installation
============
Install the package with pypi.

  $ pip install egn

Usage
=====
Use it as command line or python package.
Here are the options:

Python package
--------------
::

  import egn

  # Validate
  egn.validate(123123123)
  >>> 123123123 is invalid!

  # Parsing
  egn.parse(1234567890)
  >>> ....

  # Generating
  egn.generate()
  >>> ....

  # Generating with options
  egn_options = {'year': 1999, 'month': 3, 'day': 3, 'region': 'Sofia', 'sex': 'm'}
  egn.generate(egn_options)
  >>> ....


Command line
------------
Invoke the package with simply typing *egn*:

  $ egn

Which will print the help message.
Here are the most common commands:

::

  # Validate
  $ egn 1234567890

  # Parse
  $ egn -p 1234567890
  
  # Generate
  $ egn -g # random without options
  $ egn -g -y 1999 -m 3 -d 3 -r Sofia -s male # with options

to-do
=====
 * First step: validation
