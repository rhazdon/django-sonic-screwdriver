===
Git
===

.. TODO: Add description

Settings
========

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
    'GIT_STAGING_PRE_TAG': 'staging',
    'GIT_ACTIVATE_PRE_TAG': 'activate',

    'SECURE_TAGGING': True,
  }

Description
------------

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
| GIT_DIR               | settings.BASE_DIR | Specify your project root dir.                                      |
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
