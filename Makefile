.PHONY: test makemessages

default: help

help:
	@echo 'make targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-13s %s\n", $$1, $$2}'
	@echo '  help          This message'

test:  ## Run all tests and report the coverage.
	DJANGO_SETTINGS_MODULE=tests.settings pipenv run coverage run --source='.' manage.py test tests && pipenv run coverage html && pipenv run coverage report -m

makemessages:  ## Creates .po files of the marked strings for translating.
	pipenv run ./manage.py makemessages --locale=de
