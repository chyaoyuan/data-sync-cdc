import re


def get_re_result(result: re.search) -> str or None:
    try:
        return result.group()
    except AttributeError:
        return None