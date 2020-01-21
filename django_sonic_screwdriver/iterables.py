import collections

from django.http import QueryDict


def count(iterable):
    """
    Counts the numbers of elements of the iterable.
    """
    if hasattr(iterable, "__len__"):
        return len(iterable)

    d = collections.deque(enumerate(iterable, 1), maxlen=1)
    return d[0][0] if d else 0


def is_iterable(obj):
    """
    Check if obj is iterable.
    """
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def get_iterable(data):
    """
    Returns iterable data.
    """
    if isinstance(data, QueryDict):
        return data.lists()
    else:
        return data.items()
