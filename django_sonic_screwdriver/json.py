import collections
import copy
import json


def parse_request(request):
    """
    Parses JSON bodies safely.
    """
    try:
        body = json.loads(request.body.decode("utf-8"))
        return body
    except Exception:
        return None


def stringify_keys(dictionary: dict):
    """
    This helper function will stringify all keys in the given
    dictionary.

    For example:
        > from apps.authentication.models.user import Jobs
        > data = { Jobs.PTA: True }
        > stringify_keys(data)
        { "PTA": True }
    """
    origin_dict = copy.deepcopy(dictionary)
    return_dict = collections.defaultdict()

    for key in origin_dict.keys():

        # Check if the value is a dict
        if isinstance(origin_dict[key], dict) and origin_dict[key]:
            value = stringify_keys(copy.deepcopy(origin_dict[key]))
        else:
            value = copy.deepcopy(origin_dict[key])

        if not isinstance(key, str):
            new_key = str(key)
            if hasattr(key, "json_repr") and callable(key.json_repr):
                new_key = key.json_repr()
            return_dict[new_key] = value
        else:
            return_dict[key] = value

    return return_dict
