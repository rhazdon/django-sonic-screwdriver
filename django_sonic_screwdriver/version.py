import os
import re
import fileinput

from django_sonic_screwdriver.settings import APISettings
from django_sonic_screwdriver.utils import Shell

RELEASE_TAGS = {
	# pre-release
	'ALPHA': 'a',
	'BETA': 'b',
	'RC': 'rc',
	# dev-release
	'DEV': 'dev',
	# post-release
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
			raise FileNotFoundError
		except ValueError:
			Shell.fail('Version not found in file ' + version_file + '!')
			raise ValueError
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

	@staticmethod
	def get_patch_version(version):
		try:
			patch = version.split('.', 5)[2]
		except IndexError:
			Shell.fail('Take note your version looks like this: 0.1.2!')
			raise IndexError
		return patch

	# @staticmethod
	# def get_currently_used_pre_release_separator(patch):
	# 	separator = ''
	# 	if APISettings.PATCH_PRE_RELEASE_SEPARATOR != '':
	# 		separator = str(patch.split(APISettings.PATCH_PRE_RELEASE_SEPARATOR, 2))
	#
	# 	if separator.__len__() > 1:
	# 		return print(separator)
	# 	else:
	# 		return print('1')

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

	def set_patch(self, release_tag=''):
		"""
		Increment the patch number of project

		:var release_tag describes the tag ('a', 'b', 'rc', ...)
		:var release_tag_version describes the number behind the 'a', 'b' or 'rc'
		For e.g.:
		"""

		old_version = self.get_version()
		patch = self.get_patch_version(old_version)

		# If the release_tag is not '', try to catch the tag
		if release_tag != '':
			try:
				# patch already contains a release_tag. Just increase the release_tag_version
				release_tag_version = int(patch.split(release_tag, 2)[1])+1
				patch = str(patch.split(release_tag, 2)[0]) + str(release_tag) + str(release_tag_version)
			except IndexError:
				try:
					# patch doesn't contains any tag, so we have to add one and increase the whole patch
					patch = str(int(patch)+1) + release_tag + str(1)
				except ValueError:
					# change tag in patch (e.g. 1.2.3a1 --> 1.2.3b1)
					for key in RELEASE_TAGS:
						if RELEASE_TAGS[key] in patch:
							try:
								patch = str(patch.split(RELEASE_TAGS[key], 2)[0])
							except ValueError:
								pass
					patch = str(patch) + release_tag + str(1)

		# Standard patch (e.g. 0.1.2 --> 0.1.3)
		else:
			try:
				patch = int(patch)+1
			except ValueError:
				for key in RELEASE_TAGS:
					if RELEASE_TAGS[key] in patch:
						try:
							patch = patch.split(RELEASE_TAGS[key], 2)[0]
						except ValueError:
							pass

		new_version = str(int(old_version.split('.', 5)[0])) + '.' + \
			str(int(old_version.split('.', 5)[1])) + '.' + \
			str(patch)
		self.set_version(old_version, new_version)

	def __init__(self, release_tags=None):
		self.release_tags = release_tags or RELEASE_TAGS

	def __getattr__(self, attr):
		if attr not in self.release_tags.keys():
			raise AttributeError("Invalid VersionHandler Key: '%s'" % attr)

		val = self.release_tags[attr]
		return val

Version = Version(RELEASE_TAGS)
