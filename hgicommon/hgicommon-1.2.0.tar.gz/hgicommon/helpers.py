from uuid import uuid4


def create_random_string(postfix: str= "", prefix: str="") -> str:
    """
    Creates a random string.
    :param postfix: optional postfix
    :param prefix: optional prefix
    :return: created string
    """
    return "%s%s%s" % (prefix, uuid4(), postfix)
