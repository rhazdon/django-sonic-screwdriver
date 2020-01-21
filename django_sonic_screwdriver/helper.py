import collections
import random
import re
import string

from django.core.files import File
from django.http import QueryDict
from django.utils.encoding import force_text
from django.utils.functional import Promise

from .iterables import get_iterable, is_iterable

camelize_re = re.compile(r"[a-z0-9]?_[a-z0-9]")


def generate_random_string(string_length: int = 6, upper_case: bool = False) -> str:
    """
    Generates a random string of letters and digits.
    """
    letter_and_digits = string.ascii_letters + string.digits
    random_string = "".join(
        random.choice(letter_and_digits) for i in range(string_length)
    )

    if upper_case:
        return random_string.upper()
    return random_string


def camel_to_underscore(name):
    underscore_re = re.compile(r"([a-z]|[0-9]+[a-z]?|[A-Z]?)([A-Z])")
    return underscore_re.sub(r"\1_\2", name).lower()


def underscore_to_camel(match):
    """
    Cast sample_data to sampleData.
    """
    group = match.group()
    if len(group) == 3:
        return group[0] + group[2].upper()
    else:
        return group[1].upper()


def camelize(data):
    # Handle lazy translated strings.
    if isinstance(data, Promise):
        data = force_text(data)
    if isinstance(data, dict):
        new_dict = collections.OrderedDict()
        for key, value in data.items():
            if isinstance(key, Promise):
                key = force_text(key)
            if isinstance(key, str) and "_" in key and key[0] != "_":
                new_key = re.sub(camelize_re, underscore_to_camel, key)
            else:
                new_key = key
            new_dict[new_key] = camelize(value)
        return new_dict
    if is_iterable(data) and not isinstance(data, str):
        return [camelize(item) for item in data]
    return data


def underscoreize(data):
    """
    Underscoring data.
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in get_iterable(data):
            if isinstance(key, str):
                new_key = camel_to_underscore(key)
            else:
                new_key = key
            new_dict[new_key] = underscoreize(value)

        if isinstance(data, QueryDict):
            new_query = QueryDict(mutable=True)
            for key, value in new_dict.items():
                new_query.setlist(key, value)
            return new_query
        return new_dict
    if is_iterable(data) and not isinstance(data, (str, File)):
        return [underscoreize(item) for item in data]

    return data


def cast_ordered_dict_to_dict(ordered_dict):
    """
    This helper functions casts an OrderedDict recursively into a dict.

    :param ordered_dict:
    :return:
    """
    if not isinstance(ordered_dict, collections.OrderedDict):
        raise ValueError("Parameter `ordered_dict` is not an instance of OrderedDict.")

    for key, value in ordered_dict.items():
        if isinstance(value, collections.OrderedDict):
            ordered_dict[key] = cast_ordered_dict_to_dict(value)
    return dict(ordered_dict)


def parse_secret_from_authentication_url(url):
    """
    This helper will parse the secret part of a totp url like
    otpauth://totp/alice%07c%40apothekia.de?secret=M3FAFWGD2QA5JJPCPWEOKALPBROHXOL3&algorithm=SHA1&digits=6&period=30
    """
    return url.split("secret")[1][1:33]
