=========
Iterables
=========

`count(obj)`
============

Returns the number of items.

.. code:: python

    from django_sonic_screwdriver.iterables import get_iterable

    my_dict = {"key": "value"}
    get_iterable(my_dict)  # dict_items([('key', 'value')])


`get_iterable(obj)`
===================

Returns the iterable data. Generic handler for iterables and
`QueryDicts <https://docs.djangoproject.com/en/3.0/ref/request-response/#django.http.QueryDict>`_.

.. code:: python

    from django_sonic_screwdriver.iterables import get_iterable

    my_dict = {"key": "value"}
    get_iterable(my_dict)  # dict_items([('key', 'value')])


`is_iterable(obj)`
==================

Checks whether the given object is iterable.

.. code:: python

    from django_sonic_screwdriver.iterables import is_iterable

    my_dict = {}
    is_iterable(my_dict)  # True