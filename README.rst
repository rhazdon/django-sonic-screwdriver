Django Sonic Screwdriver
========================

.. image:: https://coveralls.io/repos/rhazdon/django-sonic-screwdriver/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/rhazdon/django-sonic-screwdriver?branch=master

.. image:: https://codeclimate.com/github/rhazdon/django-sonic-screwdriver/badges/gpa.svg
   :target: https://codeclimate.com/github/rhazdon/django-sonic-screwdriver
   :alt: Code Climate

.. image:: https://badge.fury.io/py/django-sonic-screwdriver.svg
    :target: http://badge.fury.io/py/django-sonic-screwdriver


Django Sonic Screwdriver is a collection of very useful commands and will make your life easier.


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


Settings
--------

.. code:: python

  SONIC_SCREWDRIVER = {
    # For test purpose
    'DEBUG': False,

    # Returns file where the version number is located
    'VERSION_FILE': 'setup.py',

    'PRE_RELEASE_SEPARATOR': '',  # '_', '-', '.'

    'PATCH_AUTO_TAG': False,
    'PATCH_AUTO_TAG_PUSH': False,
    'PATCH_AUTO_COMMIT': False,

    'GIT_DIR': setting.BASE_DIR,

    # Git Tagging
    'GIT_TAG_AUTO_COMMIT': False,
    'GIT_TAG_AUTO_TAG_PUSH': False,

    'GIT_STAGING_PRE_TAG': 'staging',
    'GIT_ACTIVATE_PRE_TAG': 'activate',
  }


Commands
--------

$ ./manage.py cache:clear
~~~~~~~~~~~~~~~~~~~~~~~~~~
  --default                 Clear cache


$ ./manage.py gen:secretkey
~~~~~~~~~~~~~~~~~~~~~~~~~~
  --default                 Generate a new Secretkey for Django


$ ./manage.py patch
~~~~~~~~~~~~~~~~~~~
  -M, --major               Set major number
  -m, --minor               Set minor number
  -p, --patch               Set patch number
  -d, --dev                 Set dev release (e.g. 1.2.1dev1)
  -a, --alpha               Set alpha release (e.g. 1.2.1a1)
  -b, --beta                Set beta release (e.g. 1.2.1b1)
  -r, --release-candidate   Set release candidate release (e.g. 1.2.1rc1)
  -f, --force               Force patching


$ ./manage.py git:tag
~~~~~~~~~~~~~~~~~~~~~
  --default                 (is default)
  --staging                 Create a staging tag (e.g. staging-v1.2.3)
  --activate                Create a activate tag (e.g. activate-v1.2.3)
  --push                    Push tags


$ ./manage.py git:tag:push
~~~~~~~~~~~~~~~~~~~~~~~~~~
  --default                 Push all tags


$ ./manage.py git:tag:delete
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  <tag>                     Remove the latest or given tag (optional).


$ ./manage.py pypi:export
~~~~~~~~~~~~~~~~~~~~~~~~~
  -w, --wheel               Export project with wheel (recommended)
  -u, --upload              Upload Project


$ ./manage.py pypi:upload
~~~~~~~~~~~~~~~~~~~~~~~~~
  --default                 Upload project to PyPI via twine
