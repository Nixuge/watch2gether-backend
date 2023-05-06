import random


def random_string(chars: str, length: int):
    return ''.join(random.choice(chars) for _ in range(length))