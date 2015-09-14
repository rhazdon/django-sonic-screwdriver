import os
import re
import fileinput
from subprocess import call

from django_sonic_screwdriver.settings import api_settings
from django_sonic_screwdriver.shell import Shell

PATCH_TYPE = {
	'PATCH_TYPE_NORMAL': 'n',
	'PATCH_TYPE_ALPHA': 'a',
	'PATCH_TYPE_BETA': 'b',
	'PATCH_TYPE_RC': 'rc'
}


class VersionHandler(object):
	VERSION_FILE = open(os.path.join(os.path.abspath(api_settings.VERSION_FILE))).read()

	@classmethod
	def get_version(cls):
		"""
		Return version from setup.py
		"""
		try:
			print(Shell.OKBLUE, 'Checking current version... ', Shell.ENDC)
			version = re.search(r"version=['\"]([^'\"]+)['\"]", cls.VERSION_FILE).group(1)
			print(Shell.OKBLUE, 'Current version ' + version, Shell.ENDC)
			return version
		except FileNotFoundError:
			print(Shell.WARNING, 'File not found!', Shell.ENDC)
			return False
		except ValueError:
			print(Shell.WARNING, 'Version not found in file ' + cls.VERSION_FILE + '!', Shell.ENDC)
			return False
		except:
			print(Shell.WARNING, 'Unexpected Error!', Shell.ENDC)
			return False

	@classmethod
	def set_version(cls, old_version, new_version):
		"""
		Write new version into VERSION_FILE
		"""
		try:
			for line in fileinput.input(os.path.abspath(api_settings.VERSION_FILE), inplace=True):
				print(line.replace(old_version, new_version), end='')
			print(Shell.OKGREEN, '* ' + old_version + ' --> ' + new_version, Shell.ENDC)
		except FileNotFoundError:
			print(Shell.WARNING, 'File not found!', Shell.ENDC)
		except:
			print(Shell.WARNING, 'Unexpected Error!', Shell.ENDC)

	@classmethod
	def set_major(cls):
		"""
		Increment the major number of project
		"""
		old_version = cls.get_version()
		new_version = str(int(old_version.split('.', 5)[0])+1) + '.0.0'
		cls.set_version(old_version, new_version)

	@classmethod
	def set_minor(cls):
		"""
		Increment the minor number of project
		"""
		old_version = cls.get_version()
		new_version = str(int(old_version.split('.', 5)[0])) + '.' + \
			str(int(old_version.split('.', 5)[1])+1) + '.0'
		cls.set_version(old_version, new_version)

	@classmethod
	def set_patch(cls, patch_type):
		"""
		Increment the patch number of project

		:var patch_suffix describes the number behind the 'a', 'b' or 'rc'
		:var patch_type describes, which type of patch should be used.
		For e.g.:
		PATCH_TYPE_NORMAL increases the patch number normally.
		PATCH_TYPE_ALPHA sets an 'a' at the end or increases the number behind the 'a'.
		"""
		old_version = cls.get_version()
		patch = ''

		try:
			patch = old_version.split('.', 5)[2]
		except IndexError:
			exit(Shell.FAIL + 'Take note your version looks like this: 0.1.2!' + Shell.ENDC)

		""" If the patch_type is not normal, try to catch the patch_suffix """
		if patch_type != 'n':
			try:
				# patch already contains a tag. Just increase the patch_suffix
				patch_suffix = int(patch.split(patch_type, 2)[1])+1
				patch = str(patch.split(patch_type, 2)[0]) + str(patch_type) + str(patch_suffix)
			except IndexError:
				try:
					# patch doesn't contains any tag, so we have to add it and increase the whole patch
					patch = str(int(patch)+1) + patch_type + str(1)
				except ValueError:
					# change tag in patch (e.g. 1.2.3a1 --> 1.2.3b1)
					for key in PATCH_TYPE:
						if PATCH_TYPE[key] in patch:
							try:
								patch = str(patch.split(PATCH_TYPE[key], 2)[0])
							except ValueError:
								pass
					patch = str(patch) + patch_type + str(1)

		# Standard patch (e.g. 0.1.2 --> 0.1.3)
		else:
			try:
				patch = int(patch)+1
			except ValueError:
				# Standard patch (e.g. 0.1.2a2 --> 0.1.2)
				for key in PATCH_TYPE:
					if PATCH_TYPE[key] in patch:
						try:
							patch = patch.split(PATCH_TYPE[key], 2)[0]
						except ValueError:
							pass

		new_version = str(int(old_version.split('.', 5)[0])) + '.' + \
			str(int(old_version.split('.', 5)[1])) + '.' + \
			str(patch)
		cls.set_version(old_version, new_version)

	def __init__(self, patch_type=None):
		self.patch_type = patch_type or PATCH_TYPE

	def __getattr__(self, attr):
		if attr not in self.patch_type.keys():
			raise AttributeError("Invalid VersionHandler Key: '%s'" % attr)

		val = self.patch_type[attr]
		setattr(self, attr, val)
		return val

version_handler = VersionHandler(PATCH_TYPE)
