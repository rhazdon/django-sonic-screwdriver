import binascii
import os
import random
import string
import uuid


def generate_key(length: int = 20):
    """
    Generates a random key (used for access tokens).

    :param length:
    :return:
    """
    return binascii.hexlify(os.urandom(length)).decode()


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


def generate_random_uuid4() -> uuid.UUID:
    """
    Generates a uuid4.
    """
    return uuid.uuid4()
