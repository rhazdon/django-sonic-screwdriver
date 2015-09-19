# Django Sonic Screwdriver
---------------------------------------
[![Code Climate](https://codeclimate.com/github/rhazdon/django-sonic-screwdriver/badges/gpa.svg)](https://codeclimate.com/github/rhazdon/django-sonic-screwdriver)

## !!! Still in Development !!!

Django Sonic Screwdriver is a collection of very useful commands and will make your life easier.

## Installation
You can download the latest version from the Python Package Index [PyPI](https://pypi.python.org/pypi/django-sonic-screwdriver).

	$ pip install django-sonic-screwdriver

Add the package to your settings.py:
	
	INSTALLED_APPS = (
		...
    	'django_sonic_screwdriver',
    	...
	)
	
## Settings

	SONIC_SCREWDRIVER = {
		# Returns file where the version number is located
		'VERSION_FILE': 'setup.py',
	
		'PATCH_AUTO_TAG': False,
		'PATCH_AUTO_TAG_PUSH': False,
		'PATCH_AUTO_COMMIT': False,
	
		# Git Tagging
		'GIT_TAG_AUTO_COMMIT': False,
		'GIT_TAG_AUTO_TAG_PUSH': False,
	
		'GIT_STAGING_PRE_TAG': 'staging',
		'GIT_ACTIVATE_PRE_TAG': 'activate',
	}


## Commands

	$ ./manage.py patch
		-M, --major           Set major number
		-m, --minor           Set minor number
		-p, --patch           Set patch number
		-d, --dev             Set dev release (e.g. 1.2.1dev1)
		-a, --alpha           Set alpha release (e.g. 1.2.1a1)
		-b, --beta            Set beta release (e.g. 1.2.1b1)
		-r, --release-candidate
							  Set release candidate release (e.g. 1.2.1rc1).
		-f, --force           


	$ ./manage.py git:tag
		--default             (is default)
  		--staging             Create a staging tag (e.g. staging-v1.2.3)
  		--activate            Create a activate tag (e.g. activate-v1.2.3)
  		-d, --delete-last     Delete last tag
 		--push                Push tags

