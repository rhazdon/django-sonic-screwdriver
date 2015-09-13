import os
import re


def get_setup_file():
	return open(os.path.join(os.path.abspath('setup.py'))).read()


def get_version():
	return re.search(r"version=['\"]([^'\"]+)['\"]", get_setup_file()).group(1)


def set_version():
	pass

