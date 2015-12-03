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


Settings
--------

.. code:: python

  SONIC_SCREWDRIVER = {
    # For test purpose
    'DEBUG': False,

    # Returns file where the version number is located
    'VERSION_FILE': 'setup.py',

    'RELEASE_SEPARATOR': '',  # '_', '-', '.'

    'PATCH_AUTO_TAG': False,
    'PATCH_AUTO_TAG_PUSH': False,
    'PATCH_AUTO_COMMIT': False,

    'GIT_DIR': setting.BASE_DIR,

    # Git Tagging
    'GIT_TAG_AUTO_COMMIT': False,
    'GIT_TAG_AUTO_TAG_PUSH': False,

    'GIT_STAGING_PRE_TAG': 'staging',
    'GIT_ACTIVATE_PRE_TAG': 'activate',

    'SECURE_TAGGING': True,
  }

**Description:**

+-----------------------+-------------------+---------------------------------------------------------------------+
| Setting               | Default           | Description                                                         |
+=======================+===================+=====================================================================+
| DEBUG                 | False             | Enables or disables the debug mode. For testing purposes.           |
+-----------------------+-------------------+---------------------------------------------------------------------+
| VERSION_FILE          | 'setup.py'        | Specifies, where you safe your project Version. It should be just   |
|                       |                   | on place - any other should refer to this one.                      |
+-----------------------+-------------------+---------------------------------------------------------------------+
| RELEASE_SEPARATOR     | ''                | The RELEASE_SEPARATOR is the seperator between the version number   |
|                       |                   | and the relase. E.g. v0.1.2b0, v0.1.2_b0,   v0.1.2-b0, v0.1.2.b0.   |
|                       |                   | All of this variants is support by                                  |
|                       |                   | PEP 0440<https://www.python.org/dev/peps/pep-0440/>.                |
+-----------------------+-------------------+---------------------------------------------------------------------+
| PATCH_AUTO_TAG        | False             | If True, Sonic Screwdriver tries to create automatically a tag from |
|                       |                   | every patch you create with ./manage.py patch.                      |
+-----------------------+-------------------+---------------------------------------------------------------------+
| PATCH_AUTO_TAG_PUSH   | False             | If True, after creating a tag via './manage.py patch',              |
|                       |                   | Sonic Screwdriver will try to push this tag automatically.          |
+-----------------------+-------------------+---------------------------------------------------------------------+
| PATCH_AUTO_COMMIT     | False             | NOT IMPLEMENTED YET!                                                |
+-----------------------+-------------------+---------------------------------------------------------------------+
| GIT_DIR               | settings.BASE_DIR | Specify your project root dir.                                      |
+-----------------------+-------------------+---------------------------------------------------------------------+
| GIT_TAG_AUTO_COMMIT   | False             | NOT IMPLEMENTED YET!                                                |
+-----------------------+-------------------+---------------------------------------------------------------------+
| GIT_TAG_AUTO_TAG_PUSH | False             | If True, Sonic Screwdriver pushes automatically the current         |
|                       |                   | created tags.                                                       |
+-----------------------+-------------------+---------------------------------------------------------------------+
| GIT_STAGING_PRE_TAG   | 'staging'         | Pre tag for git.                                                    |
+-----------------------+-------------------+---------------------------------------------------------------------+
| GIT_ACTIVATE_PRE_TAG  | 'activate'        | Pre tag for git.                                                    |
+-----------------------+-------------------+---------------------------------------------------------------------+
| SECURE_TAGGING        | True              | Security for production tags. If True, Sonic Screwdriver checks the |
|                       |                   | remote repository for a staging tag of the current requested        |
|                       |                   | production version. Developer will be able to create a production   |
|                       |                   | tag only then, if the same version exists as staging tag.           |
+-----------------------+-------------------+---------------------------------------------------------------------+


Commands
--------

cache:clear
~~~~~~~~~~~
Clear the cache.


gen:secretkey
~~~~~~~~~~~~~
Generate a new Secretkey for Django.


patch
~~~~~
Command "patch" will help you to increase the version number of your project in a easy way.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| -M, --major               | Set major number                              |
+---------------------------+-----------------------------------------------+
| -m, --minor               | Set minor number                              |
+---------------------------+-----------------------------------------------+
| -p, --patch               | Set patch number                              |
+---------------------------+-----------------------------------------------+
| -d, --dev                 | Set dev release (e.g. 1.2.1dev1)              |
+---------------------------+-----------------------------------------------+
| -a, --alpha               | Set alpha release (e.g. 1.2.1a1)              |
+---------------------------+-----------------------------------------------+
| -b, --beta                | Set beta release (e.g. 1.2.1b1)               |
+---------------------------+-----------------------------------------------+
| -r, --release-candidate   | Set release candidate release (e.g. 1.2.1rc1) |
+---------------------------+-----------------------------------------------+
| -f, --force               | Force patching                                |
+---------------------------+-----------------------------------------------+


git:add
~~~~~~~
Add files to Git repository. Supports all standard "git add" options.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| -n, --dry-run             | Dry run                                       |
+---------------------------+-----------------------------------------------+
| --verbose                 | Be verbose.                                   |
+---------------------------+-----------------------------------------------+
| -i, --interactive         | Interactive picking.                          |
+---------------------------+-----------------------------------------------+
| -p, --patch               | Select hunks interactively.                   |
+---------------------------+-----------------------------------------------+
| -e, --edit                | Edit current diff and apply.                  |
+---------------------------+-----------------------------------------------+
| -f, --force               | Allow adding otherwise ignored files.         |
+---------------------------+-----------------------------------------------+
| -u, --update              | Update tracked files.                         |
+---------------------------+-----------------------------------------------+
| -N, --intent-to-add       | Record only the fact that the path will be    |
|                           | added later.                                  |
+---------------------------+-----------------------------------------------+
| -A, --all                 | Add changes from all tracked and untracked    |
|                           | files.                                        |
+---------------------------+-----------------------------------------------+
| --ignore-removal          | Ignore paths removed in the working tree      |
|                           | (same as --no-all).                           |
+---------------------------+-----------------------------------------------+
| --refresh                 | Do not add, only refresh the index.           |
+---------------------------+-----------------------------------------------+
| --ignore-errors           | Just skip files which cannot be added because |
|                           | of errors.                                    |
+---------------------------+-----------------------------------------------+
| --ignore-missing          | Check if - even missing - files are ignored   |
|                           | in dry run.                                   |
+---------------------------+-----------------------------------------------+


git:tag
~~~~~~~
Tag your project.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| --default                 | (is default)                                  |
+---------------------------+-----------------------------------------------+
| --staging                 | Create a staging tag (e.g. staging-v1.2.3).   |
+---------------------------+-----------------------------------------------+
| --activate                | Create a activate tag (e.g. activate-v1.2.3). |
+---------------------------+-----------------------------------------------+
| --push                    | Push tags.                                    |
+---------------------------+-----------------------------------------------+


git:tag:push
~~~~~~~~~~~~
Push your tagged project.


git:tag:delete
~~~~~~~~~~~~~~
Remove the latest or given tag from local repository.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| <tag>                     | Remove the latest or given tag (optional).    |
+---------------------------+-----------------------------------------------+


pypi:export
~~~~~~~~~~~
Export your project.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| --no-wheel                | Export project without wheel.                 |
|                           | (not recommended)                             |
+---------------------------+-----------------------------------------------+
| -u, --upload              | Upload Project.                               |
+---------------------------+-----------------------------------------------+


pypi:upload
~~~~~~~~~~~
Upload project to pypi via twine.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| --default                 | Upload project to PyPI via twine.             |
+---------------------------+-----------------------------------------------+


To Do:
------
[x] git:add

[x] Secure production tagging

[ ] git:commit

[ ] Heroku Support

[ ] Deis Support

[ ] Docker and Vagrant blueprints

[ ] ...
