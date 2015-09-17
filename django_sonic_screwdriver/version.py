import os
import re
import fileinput

from django_sonic_screwdriver.settings import APISettings
from django_sonic_screwdriver.utils import Shell

PATCH_OPTIONS = {
	'PATCH_NORMAL': 'n',
	'PATCH_DEV': 'dev',
	'PATCH_ALPHA': 'a',
	'PATCH_BETA': 'b',
	'PATCH_RC': 'rc'
}


class Version(object):

	@staticmethod
	def get_version():
		"""
		Return version from setup.py
		"""
		version_desc = open(os.path.join(os.path.abspath(APISettings.VERSION_FILE)))
		version_file = version_desc.read()

		try:
			version = re.search(r"version=['\"]([^'\"]+)['\"]", version_file).group(1)
			return version
		except FileNotFoundError:
			Shell.fail('File not found!')
			return False
		except ValueError:
			Shell.fail('Version not found in file ' + version_file + '!')
			return False
		finally:
			version_desc.close()

	@staticmethod
	def set_version(old_version, new_version):
		"""
		Write new version into VERSION_FILE
		"""
		try:
			for line in fileinput.input(os.path.abspath(APISettings.VERSION_FILE), inplace=True):
				print(line.replace(old_version, new_version), end='')
			Shell.success('* ' + old_version + ' --> ' + new_version)
		except FileNotFoundError:
			Shell.warn('File not found!')

	def set_major(self):
		"""
		Increment the major number of project
		"""
		old_version = self.get_version()
		new_version = str(int(old_version.split('.', 5)[0])+1) + '.0.0'
		self.set_version(old_version, new_version)

	def set_minor(self):
		"""
		Increment the minor number of project
		"""
		old_version = self.get_version()
		new_version = str(int(old_version.split('.', 5)[0])) + '.' + \
			str(int(old_version.split('.', 5)[1])+1) + '.0'
		self.set_version(old_version, new_version)

	def set_patch(self, patch_option):
		"""
		Increment the patch number of project

		:var patch_suffix describes the number behind the 'a', 'b' or 'rc'
		:var patch_type describes, which type of patch should be used.
		For e.g.:
		PATCH_TYPE_NORMAL increases the patch number normally.
		PATCH_TYPE_ALPHA sets an 'a' at the end or increases the number behind the 'a'.
		"""

		old_version = self.get_version()
		patch = ''

		try:
			patch = old_version.split('.', 5)[2]
		except IndexError:
			# TODO: Raise Error!
			exit(Shell.FAIL + 'Take note your version looks like this: 0.1.2!' + Shell.ENDC)

		""" If the patch_type is not normal, try to catch the patch_suffix """
		if patch_option != 'n':
			try:
				# patch already contains a tag. Just increase the patch_suffix
				patch_suffix = int(patch.split(patch_option, 2)[1])+1
				patch = str(patch.split(patch_option, 2)[0]) + str(patch_option) + str(patch_suffix)
			except IndexError:
				try:
					# patch doesn't contains any tag, so we have to add it and increase the whole patch
					patch = str(int(patch)+1) + patch_option + str(1)
				except ValueError:
					# change tag in patch (e.g. 1.2.3a1 --> 1.2.3b1)
					for key in PATCH_OPTIONS:
						if PATCH_OPTIONS[key] in patch:
							try:
								patch = str(patch.split(PATCH_OPTIONS[key], 2)[0])
							except ValueError:
								pass
					patch = str(patch) + patch_option + str(1)

		# Standard patch (e.g. 0.1.2 --> 0.1.3)
		else:
			try:
				patch = int(patch)+1
			except ValueError:
				# Standard patch (e.g. 0.1.2a2 --> 0.1.2)
				for key in PATCH_OPTIONS:
					if PATCH_OPTIONS[key] in patch:
						try:
							patch = patch.split(PATCH_OPTIONS[key], 2)[0]
						except ValueError:
							pass

		new_version = str(int(old_version.split('.', 5)[0])) + '.' + \
			str(int(old_version.split('.', 5)[1])) + '.' + \
			str(patch)
		self.set_version(old_version, new_version)

	def __init__(self, patch_options=None):
		self.patch_options = patch_options or PATCH_OPTIONS

	def __getattr__(self, attr):
		if attr not in self.patch_options.keys():
			raise AttributeError("Invalid VersionHandler Key: '%s'" % attr)

		val = self.patch_options[attr]
		return val

Version = Version(PATCH_OPTIONS)
