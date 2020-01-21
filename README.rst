Django Sonic Screwdriver
========================

.. image:: https://coveralls.io/repos/github/rhazdon/django-sonic-screwdriver/badge.svg
   :target: https://coveralls.io/github/rhazdon/django-sonic-screwdriver

.. image:: https://codeclimate.com/github/rhazdon/django-sonic-screwdriver/badges/gpa.svg
   :target: https://codeclimate.com/github/rhazdon/django-sonic-screwdriver
   :alt: Code Climate

.. image:: https://badge.fury.io/py/django-sonic-screwdriver.svg
   :target: http://badge.fury.io/py/django-sonic-screwdriver

.. image:: https://travis-ci.org/rhazdon/django-sonic-screwdriver.svg?branch=master
   :target: https://travis-ci.org/rhazdon/django-sonic-screwdriver

Django Sonic Screwdriver is a collection of very useful commands and will make your life easier.

The versioning tool fully supports PEP 0440 <https://www.python.org/dev/peps/pep-0440/>.


Installation
------------
You can download the latest version from the Python Package Index PyPI.

.. code:: bash

  $ pip install django-sonic-screwdriver


Add the package to your settings.py:

.. code:: python

  INSTALLED_APPS = (
    ...
    'django_sonic_screwdriver',
    ...
  )




To Do:
------
[x] git:add

[x] Secure production tagging

[ ] git:commit

[ ] Heroku Support

[ ] Deis Support

[ ] Docker and Vagrant blueprints

[ ] ...
