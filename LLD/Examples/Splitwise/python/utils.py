""" helper methods """
import random, string


def unique_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=16))
