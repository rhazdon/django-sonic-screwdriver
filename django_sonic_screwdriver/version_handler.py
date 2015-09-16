import os
import re
import fileinput

from django_sonic_screwdriver.settings import api_settings
from django_sonic_screwdriver.shell import Shell

PATCH_OPTIONS = {
	'PATCH_NORMAL': 'n',
	'PATCH_DEV': 'dev',
	'PATCH_ALPHA': 'a',
	'PATCH_BETA': 'b',
	'PATCH_RC': 'rc'
}


class VersionHandler(object):

	@classmethod
	def get_version(cls):
		"""
		Return version from setup.py
		"""
		version_desc = open(os.path.join(os.path.abspath(api_settings.VERSION_FILE)))
		version_file = version_desc.read()

		try:
			version = re.search(r"version=['\"]([^'\"]+)['\"]", version_file).group(1)
			return version
		except FileNotFoundError:
			print(Shell.WARNING, 'File not found!', Shell.ENDC)
			return False
		except ValueError:
			print(Shell.WARNING, 'Version not found in file ' + version_file + '!', Shell.ENDC)
			return False
		except:
			print(Shell.WARNING, 'Unexpected Error!', Shell.ENDC)
			return False
		finally:
			version_desc.close()

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
	def set_patch(cls, patch_option):
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
		cls.set_version(old_version, new_version)

	def __init__(self, patch_options=None):
		self.patch_options = patch_options or PATCH_OPTIONS

	def __getattr__(self, attr):
		if attr not in self.patch_options.keys():
			raise AttributeError("Invalid VersionHandler Key: '%s'" % attr)

		val = self.patch_options[attr]
		return val

VersionHandler = VersionHandler(PATCH_OPTIONS)
