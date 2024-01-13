import random
import string


def random_lower_string(k: int = 32) -> str:
    """Generate random string with lowercase letters

    `k`: length of string
    """
    return "".join(random.choices(string.ascii_lowercase, k=k))
