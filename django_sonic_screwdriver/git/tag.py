from subprocess import call
from django_sonic_screwdriver.git.base import get_version


def git_tag():
	call(['git', 'branch'])


def increase_major():
	'''
	Increment the major number of project
	'''
	version = int(get_version().split('.', 5)[0])+1
	print(version)


def increase_minor():
	'''
	Increment the minor number of project
	'''
	version = int(get_version().split('.', 5)[1])+1
	print(version)


def increase_revision():
	'''
	Increment the revision number of project
	'''
	version = int(get_version().split('.', 5)[2])+1
	print(version)
