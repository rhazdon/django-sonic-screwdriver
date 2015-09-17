from django.conf import settings


USER_SETTINGS = getattr(settings, 'SONIC_SCREWDRIVER', None)

DEFAULTS = {
	# Returns file where the version number is located
	'VERSION_FILE': 'setup.py',

	'PATCH_AUTO_TAG': False,
	'PATCH_AUTO_TAG_PUSH': False,

	# Git
	'GIT_TAG_AUTO_COMMIT': False,
	'GIT_TAG_AUTO_PUSH': False,

	'GIT_AUTO_BRANCH': False,
	'GIT_AUTO_COMMIT': False,
	'GIT_AUTO_COMMIT_PUSH': False,
	'GIT_AUTO_TAG': False,
	'GIT_AUTO_TAG_COMMIT': False,
	'GIT_AUTO_TAG_PUSH': False,
	'GIT_STAGING_TAG': 'staging',
	'GIT_ACTIVATE_TAG': 'activate',
}


class APISettings(object):
	"""
	A settings object, that allows API settings to be accessed as properties.
	For example:
	from django_sonic_screwdriver.settings import api_settings
	print(api_settings.ANY_VALUE)
	"""
	def __init__(self, user_settings=None, defaults=None):
		self.user_settings = user_settings or {}
		self.defaults = defaults or DEFAULTS

	def __getattr__(self, attr):
		if attr not in self.defaults.keys():
			raise AttributeError("Invalid API setting: '%s'" % attr)

		try:
			# Check if present in user settings
			val = self.user_settings[attr]
		except KeyError:
			# Fall back to defaults
			val = self.defaults[attr]

		# Cache the result
		setattr(self, attr, val)
		return val

APISettings = APISettings(USER_SETTINGS, DEFAULTS)
