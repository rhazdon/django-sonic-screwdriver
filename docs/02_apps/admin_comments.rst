==============
Admin Comments
==============

This project is highly inspired by https://github.com/jamiecounsell/django-admin-comments.

Install
=======

.. code:: bash

  $ pip install django-sonic-screwdriver


Add the package to your settings.py:

.. code:: python

  INSTALLED_APPS = (
    ...
    'django_sonic_screwdriver.apps.admin_comments',
    ...
  )

Migrate your database:

.. code:: bash

    ./manage.py migrate


Usage
=====

.. code:: python

    from django_sonic_screwdriver.apps.admin_comments.admin import CommentInline

    class MyModelAdmin(admin.ModelAdmin):
        model = MyModel
        inlines = [CommentInline]
